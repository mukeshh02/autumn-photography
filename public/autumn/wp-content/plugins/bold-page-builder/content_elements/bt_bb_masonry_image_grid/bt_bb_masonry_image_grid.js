(function( $ ) {
	"use strict";
	
	var bt_bb_masonry_image_grid_fix_resize = function() {
		$( '.bt_bb_masonry_image_grid .bt_bb_grid_item' ).each(function() {
			$( this ).height( Math.floor( $( this ).width() * $( this ).data( 'hw' ) ) );
		});
		$( '.bt_bb_masonry_image_grid' ).each( function() {
			$( this ).width( 'initial' );
			var child_margin = parseInt( $( this ).find( '.bt_bb_masonry_post_image_content' ).css( 'margin-right' ) ) + parseInt( $( this ).find( '.bt_bb_masonry_post_image_content' ).css( 'margin-left' ) );
			var base_item_width =  ( $( this ).width() - child_margin ) / ( $( this ).data( 'columns' ) ) ;
			if ( Math.ceil( base_item_width ) != base_item_width ) {
				$( this ).width( $( this ).data( 'columns' ) * Math.ceil( base_item_width ) + child_margin );
			} 				
		});

	}

	var bt_bb_masonry_image_grid_load_images = function( ) {
		$( '.bt_bb_masonry_image_grid' ).each(function() {
			var page_bottom = $( window ).scrollTop() + $( window ).height();
			$( this ).find( '.bt_bb_grid_item' ).each(function() {
				var this_top = $( this ).offset().top;
				if ( this_top < page_bottom + $( window ).height() ) {
					var img_src = $( this ).data( 'src' );
					var img_title = $( this ).data( 'title' );
					var img_src_full = $( this ).data( 'src-full' );
					var $holder = $( this ).find('.bt_bb_grid_item_inner_image');
					if ( img_src !== '' && $holder.html() == '' ) {
						// Build via DOM attributes -- data( 'title' ) returns the decoded
						// attribute value, so concatenating it into an HTML string would
						// let a crafted attachment title break out and inject markup.
						var img = $( '<img>' );
						img.attr( 'src', img_src );
						img.attr( 'title', img_title || '' );
						img.attr( 'alt', img_title || '' );
						img.attr( 'data-src-full', img_src_full );
						$holder.empty().append( img );
					}
				}
			});
		});
	}	


	$( window ).load(function() {

		bt_bb_masonry_image_grid_fix_resize();
		
		$( '.bt_bb_masonry_post_image_content' ).masonry({
			columnWidth: '.bt_bb_grid_sizer',
			itemSelector: '.bt_bb_grid_item',
			gutter: 0,
			percentPosition: true
		});
		
		bt_bb_masonry_image_grid_load_images();

		$( window ).on( 'resize', function() {
			bt_bb_masonry_image_grid_fix_resize();
		});
		
		$( window ).on( 'scroll', function() {
			bt_bb_masonry_image_grid_load_images();
		});
		
		setTimeout(function() {
			$( '.bt_bb_masonry_post_image_content' ).masonry( 'layout' );
		}, 10 );
	});

})( jQuery );