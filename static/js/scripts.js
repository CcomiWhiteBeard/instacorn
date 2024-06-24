/*!
* Start Bootstrap - Landing Page v6.0.0 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

/*!
* Start Bootstrap - Landing Page v6.0.0 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

window.addEventListener('DOMContentLoaded', event => {

	// 도서 추가 글자 수 제한
/*	$('#inputBookSummary').on('keyup', function() {
		$('#inputBookSummaryCount').html("("+$(this).val().length+" / 1000)");
		if($(this).val().length > 1000) {
			$(this).val($(this).val().substring(0, 1000));
			$('#inputBookSummaryCount').html("(1000 / 1000)");
		}
	});*/

	// 공지사항 글자 수 제한
	$('#inputNoticeContent').on('keyup', function() {
		$('#inputNoticeContentCount').html("("+$(this).val().length+" / 1000)");
		if($(this).val().length > 1000) {
			$(this).val($(this).val().substring(0, 1000));
			$('#inputNoticeContentCount').html("(1000 / 1000)");
		}
	});
	
	// 추천 도서 글자 수 제한
	$('#inputGoodContent').on('keyup', function() {
		$('#inputGoodContentCount').html("("+$(this).val().length+" / 1000)");
		if($(this).val().length > 1000) {
			$(this).val($(this).val().substring(0, 1000));
			$('#inputGoodContentCount').html("(1000 / 1000)");
		}
	});
	
	// 댓글 글자 수 제한
	$('#inputCommentContent').on('keyup', function() {
		$('#inputCommentContentCount').html("("+$(this).val().length+" / 1000)");
		if($(this).val().length > 1000) {
			$(this).val($(this).val().substring(0, 1000));
			$('#inputCommentContentCount').html("1000 / 1000)");
		}
	});
	
	// 게시글 글자 수 제한
	$('#inputBoardContent').on('keyup', function() {
		$('#inputBoardContentCount').html("("+$(this).val().length+" / 1000)");
		if($(this).val().length > 1000) {
			$(this).val($(this).val().substring(0, 1000));
			$('#inputBoardContentCount').html("(1000 / 1000)");
		}
	});
	
	
});