function doLogin(){
    if(document.form1.HAKBEON.value.length==0)
    {
        alert("아이디를 입력해 주세요.");
        document.form1.HAKBEON.focus();
        return;
    }
    
    if(document.form1.PWD.value.length==0)
    {
        alert("비밀번호를 입력해 주세요.");
        document.form1.PWD.focus();
        return;
    }

    document.form1.target = "_self";
    document.form1.action = "/common/login.do?method=login";
 	// NetFUNNEL 적용
 	NetFunnel_Action({},document.form1);
    //document.form1.submit();
} 