document.getElementById('search').addEventListener('input', function () {
let sval=this.value.toLowerCase();
let cat=document.getElementById('cat').value;
document.querySelectorAll('.subtab').forEach(table => {
        let subname=table.querySelector('.subname').textContent.toLowerCase();
        let chap=table.querySelectorAll('.crow');
        let submatch=cat==="subject" && subname.includes(sval);
        let haschapmatch=false;
        let butadd=table.nextElementSibling;
        let butdel=butadd?.nextElementSibling;
        let buted=butdel?.nextElementSibling;

        chap.forEach(row => {
            let chapname=row.querySelector('.cname').textContent.toLowerCase();
            let chapmatch=cat==="chapter" && chapname.includes(sval);

            if(chapmatch){
                haschapmatch=true;
                row.style.display="";
            } 
            else{
                row.style.display=cat==="chapter" ? "none" : "";
            }
        });

        if (submatch || haschapmatch){
            table.style.display="";
            if(butadd)
                butadd.style.display="";
            if(butdel)
                butdel.style.display="";
            if(buted)
                buted.style.display="";
        } 
        else {
            table.style.display="none";
            if(butadd)
                butadd.style.display="none";
            if(butdel)
                butdel.style.display="none";
            if(buted)
                buted.style.display="none";
        }
    });
});
        