document.addEventListener("touchstart", function() {},false);


$(function() {
  //caches a jQuery object containing the header element
  var header = $(".header-wrapper");
  $(window).scroll(function() {
      var scroll = $(window).scrollTop();

      if (scroll >= 100) {
          header.addClass("scroll");
      } else {
          header.removeClass("scroll");
      }
  });

  if(!localStorage.getItem('cookieAccepted')) {
    $('.cookies').addClass('show');
  }

  $('.accept-cookie').on('click', function() {
    $('.cookies').removeClass('show');
    localStorage.setItem('cookieAccepted', true);
  });

  $('.hamburger').on('click', function() {
    $('.hamburger').toggleClass('is-active');
    $('.navigation').toggleClass('show');
  });
  
});
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    $('.hamburger').toggleClass('is-active');
    $('.navigation').toggleClass('show');
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 300, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }

  });