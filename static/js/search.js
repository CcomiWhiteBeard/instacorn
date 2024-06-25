$(document).ready(function() {
    $('#search-input').on('keypress',function(event) {
        if(event.which == 13){
            var keyword = $('#search-input').val();
            alert('keyword ' + keyword)
            $.ajax({
                url: 'instaselect.do',
                type: 'GET',
                data: { sval : keyword} ,
                success: function(data) {
                    $('#results').empty();
                    $.each(data.hashresult, function(index,item) {
                        $('#results').append('<p>' + item.content + '</p>');
                        
                    });

                    //<h2>username1</h2>
                    //<h3>place....</h3>
                    $.each(data.justresult, function(index,item) {
                        $('#results').append(
                            '<a href="blogselect.do">' +
                                '<div class="card-heading">' +
                                    '<img class="profile" src="static/images/' + item.profileimg + '" alt="">' + 
                                
                                    '<div class="cardusername">' +
                                        '<p><b>' + item.id + '</b></p>' + 
                                        '<p class="item-name">' + item.name + '</p>' + 
                                    '</div>' +
                                '</div>' +
                            '</a>'


                        );
                        
                    });
                },
                error: function() {
                    $('#results').append('<p>검색 중 오류가 발생했습니다.</p>')
                }
            });
        }
    });
});


          
function w3_open() {
  document.getElementById("search-input").value = "";
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  var searchInput = document.getElementById("search-input");
  document.getElementById("mySidebar").style.display = "none";
  
}


























