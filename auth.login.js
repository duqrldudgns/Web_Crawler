function Auth() {
    var _this = this; // _this에 Auth라는 함수를 넣었습니다.
    _this.env = {};
    _this.env.form = $('#loginForm'); // 로그인 폼입니다. id, pw, _csrf 등을 받는다고 위에서 확인했죠?
    _this.env.iptUserId = _this.env.form.find('*[name=userId]'); // 사용자가 폼에 입력한 ID입니다.
    _this.env.iptUserPassWord = _this.env.form.find('*[name=userPassword]'); // 사용자가 폼에 입력한 PW입니다.

    _this.loginValidate = function() {
        var isValid = true; // 아무 문제가 없다면(id나 pw가 빈칸이 아니라면) true를 반환하는 함수입니다.
        if (_this.env.iptUserId.val().trim() == '') { // 아이디가 빈칸이면 false죠?
            alert('아이디를 입력하세요.');
            _this.env.iptUserId.focus();
            isValid = false;
            return isValid;
        }
        if (_this.env.iptUserPassWord.val().trim() == '') { // 비번이 빈칸이어도 false가 됩니다.
            alert('비밀번호를 입력하세요.');
            _this.env.iptUserPassWord.focus();
            isValid = false;
            return isValid;
        }
        return isValid;
    };

    _this.login = function() {
        var isValid = _this.loginValidate(); // 방금 본 아이디/비번이 빈칸인지 확인하기
        if (isValid) { // 빈칸이 아니라면 ->
            _this.env.form.attr({ // 폼 속성을 정의해 줍시다.
                method: 'POST', // 폼 전송 방식은 'POST'이고,
                action: BASE_URL + '/login' // 폼 전송하는 주소는 https://www.clien.net/service/login 이네요!
            });
            _this.env.form.submit(); // 진짜로 폼을 전송해줍니다.
        }
    };
} 
