from flask import Flask,request,redirect,render_template,url_for,session,flash
import sqlite3 as sql

app=Flask(__name__)
app.secret_key="secracy_master"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        connection=sql.connect('quiz_database.db')
        curr=connection.cursor()
        uname=request.form['uname']
        pwd=request.form['pwd']
        curr.execute('SELECT id,full_name,username from user WHERE username=? and password=?',(uname,pwd))
        u1=curr.fetchone()
        connection.close()

        if u1:
            session['uid']=u1[0]
            session['fname']=u1[1]
            session['uname']=u1[2]
            if u1[2]=='admin':
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('user_home'))
        else:
            return 'Invalid Credentials',401
        
    return render_template('login.html')

@app.route('/register',methods=["GET",'POST'])
def register():
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pwd']
        fname=request.form['fname']
        qual=request.form['qual']
        dob=request.form['dob']

        conn=sql.connect('quiz_database.db')
        curr=conn.cursor()
        curr.execute('SELECT * from user WHERE username=?',(uname,))
        exuser=curr.fetchone()

        if exuser:
            return 'user already exists',400
        
        curr.execute('''INSERT INTO user(username,password,full_name,qualification,dob)
                        VALUES (?,?,?,?,?)''',(uname,pwd,fname,qual,dob))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/admin_home',methods=["GET",'POST'])
def admin_home(): 
    if 'uid' not in session or session.get('uname')!='admin':
        return redirect(url_for('login'))
    
    conn=sql.connect('quiz_database.db')
    conn.row_factory=sql.Row
    curr=conn.cursor()
    curr.execute('SELECT id,name from subject')
    subs=curr.fetchall()
    sub_l=[]
    for sub in subs:
        sub_l.append({'id':sub['id'],'name':sub['name'],'chapters':[]})

    for sub in sub_l:
        sub_id=sub['id']
        curr.execute('''
            SELECT chapter.id,chapter.name,COUNT(question.id) AS q_count
            FROM chapter
            LEFT JOIN quiz 
            ON chapter.id=quiz.chapter_id
            LEFT JOIN question ON quiz.id=question.quiz_id
            WHERE chapter.subject_id=?
            GROUP BY chapter.id
        ''',(sub_id,))

        chaps=curr.fetchall()
        for chap in chaps:
            sub['chapters'].append({'id':chap['id'],'name':chap['name'],'q_count':chap['q_count']})

    conn.close()
    return render_template('admin_home.html',sub_l=sub_l)

@app.route('/add_sub',methods=['GET','POST'])
def add_sub():
    if 'uid' not in session or session.get('uname')!='admin':
        return redirect(url_for('login'))
    
    if request.method=='POST':
        sname=request.form['sname']
        sdesc=request.form['sdesc']
        conn=sql.connect('quiz_database.db')
        curr=conn.cursor()
        curr.execute('INSERT into subject(name,description) VALUES (?,?)',(sname,sdesc))
        conn.commit()
        conn.close()

        flash('Subject created successfully!', 'success')
        return redirect(url_for('admin_home'))

    return render_template('add_sub.html')

@app.route('/add_chap/<int:subject_id>',methods=['GET','POST'])
def add_chap(subject_id):
    if 'uid' not in session or session.get('uname')!='admin':
        return redirect(url_for('login'))
    
    conn=sql.connect('quiz_database.db')
    curr=conn.cursor()
    curr.execute('SELECT id,name from subject WHERE id=?',(subject_id,))
    subex=curr.fetchone()
    if subex:
        sub_name=subex[1]
    conn.close()

    if not subex:
        flash('Invalid Subject ID!','error')
        return redirect(url_for('admin_home'))

    if request.method=='POST':
        cname=request.form['cname']
        cdesc=request.form['cdesc']
        conn=sql.connect('quiz_database.db')
        curr=conn.cursor()
        curr.execute('INSERT into chapter(subject_id,name,description) VALUES(?,?,?)',(subject_id,cname,cdesc))
        conn.commit()
        conn.close()

        flash('Chapter created successfully!','success')
        return redirect(url_for('admin_home'))

    return render_template('add_chap.html',subject_id=subject_id,sub_name=sub_name)

@app.route('/view_quizzes/<int:chapter_id>')
def view_quizzes(chapter_id):
    if 'uid' not in session or session.get('uname')!='admin':
       return redirect(url_for('login'))
     
    conn=sql.connect('quiz_database.db')
    conn.row_factory=sql.Row
    curr=conn.cursor()
    curr.execute('SELECT name from chapter where id=?',(chapter_id,))
    chapo=curr.fetchone()

    if not chapo:
        flash('Invalid CHAPTER ID!','error')
        return redirect(url_for('admin_home'))

    chap_name=chapo['name']

    curr.execute('''
        SELECT quiz.id,question.question_title,quiz.date_of_quiz,quiz.time_duration FROM quiz
        LEFT JOIN question ON quiz.id=question,quiz_id
        WHERE chapter_id=?
        GROUP BY quiz.id
        ''',(chapter_id,))
    avail_quiz=curr.fetchall()

    conn.close()
    return render_template('view_quizzes.html',avail_quiz=avail_quiz,chap_name=chap_name,chapter_id=chapter_id)

@app.route('/user_home')
def user_home():
    if 'uid' not in session:
        return redirect(url_for('login'))
    
    conn=sql.connect('quiz_database.db')
    conn.row_factory=sql.Row
    curr=conn.cursor()
    curr.execute('SELECT id,name from subject')
    subs=curr.fetchall()
    sub_l=[]

    for sub in subs:
        sub_id=sub['id']
        sub_name=sub['name']
        curr.execute('''
            SELECT chapter.id,chapter.name,COUNT(question.id) AS q_count
            FROM chapter
            LEFT JOIN quiz 
            ON chapter.id=quiz.chapter_id
            LEFT JOIN question ON quiz.id=question.quiz_id
            WHERE chapter.subject_id=?
            GROUP BY chapter.id
        ''',(sub_id,))

        chaps=curr.fetchall()
        chap_l=[]
        for chap in chaps:
            chap_l.append({'name':chap['name'],'q_count':chap['q_count']})
        
        sub_l.append({'name':sub_name,'chapters':chap_l})
    
    conn.close()

    return render_template('user_home.html',name=session['fname'],sub_l=sub_l)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login',msg="Logged out successfully"))

if __name__=="__main__":
    app.run()