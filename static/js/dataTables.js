window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    //가볍고 확장 가능하며 종속성이없는 자바 스크립트 HTML 테이블 플러그인
    //jQuery DataTables와 유사 하지만 jQuery 종속성이 없다.
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }

	//추천 도서 게시물의 도서가 이미 존재하는지 확인하기 위해 도서 테이블을 시각화해주기 위해 테이블 하나 더 생성
    const datatablesSimple2 = document.getElementById('datatablesSimple2');
    if (datatablesSimple2) {
        new simpleDatatables.DataTable(datatablesSimple2);
    }
});
