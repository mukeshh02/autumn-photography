(function( $ ) {
	"use strict";  
	$( '.slick-slider' ).each(function() {
		console.log( $( this ) );
		$( this ).on('init reInit', function (event, slick, currentSlide, nextSlide) {
			 // var slider_id = $( this ).attr('id');
			var count = slick.slideCount;
			
			console.log( count );				 
			 $( '<li class="bt_bb_content_slider_paging">' + count + '</li>' ).insertAfter( $( this ).find('ul.slick-dots li' ).last() );
		});		
	});
})( jQuery );