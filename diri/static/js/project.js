//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function () {
  if (animating) return false;
  animating = true;

  current_fs = $(this).parent();
  next_fs = $(this).parent().next();

  //activate next step on progressbar using the index of next_fs
  $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

  //show the next fieldset
  next_fs.show();
  //hide the current fieldset with style
  current_fs.animate({ opacity: 0 }, {
    step: function (now, mx) {
      //as the opacity of current_fs reduces to 0 - stored in "now"
      //1. scale current_fs down to 80%
      scale = 1 - (1 - now) * 0.2;
      //2. bring next_fs from the right(50%)
      left = (now * 50) + "%";
      //3. increase opacity of next_fs to 1 as it moves in
      opacity = 1 - now;
      current_fs.css({
        'transform': 'scale(' + scale + ')',
        'position': 'absolute'
      });
      next_fs.css({ 'left': left, 'opacity': opacity });
    },
    duration: 800,
    complete: function () {
      current_fs.hide();
      animating = false;
    },
    //this comes from the custom easing plugin
    easing: 'easeInOutBack'
  });
});

$(".previous").click(function () {
  if (animating) return false;
  animating = true;

  current_fs = $(this).parent();
  previous_fs = $(this).parent().prev();

  //de-activate current step on progressbar
  $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

  //show the previous fieldset
  previous_fs.show();
  //hide the current fieldset with style
  current_fs.animate({ opacity: 0 }, {
    step: function (now, mx) {
      //as the opacity of current_fs reduces to 0 - stored in "now"
      //1. scale previous_fs from 80% to 100%
      scale = 0.8 + (1 - now) * 0.2;
      //2. take current_fs to the right(50%) - from 0%
      left = ((1 - now) * 50) + "%";
      //3. increase opacity of previous_fs to 1 as it moves in
      opacity = 1 - now;
      current_fs.css({ 'left': left });
      previous_fs.css({ 'transform': 'scale(' + scale + ')', 'opacity': opacity });
    },
    duration: 800,
    complete: function () {
      current_fs.hide();
      animating = false;
    },
    //this comes from the custom easing plugin
    easing: 'easeInOutBack'
  });
});

$('#pay').click(function payWithPaystackOrg(e) {
  var email = $("#id_mail").val();
  var phone = $("#id_phone").val();
  var fname = $("#id_first_name").val();
  var lname = $("#id_last_name").val();

  e.preventDefault();
  var handler = PaystackPop.setup({
    //key: "pk_test_bbf939ac50083a6842f9a88433cf6ba690b9ca09",
    key: 'pk_live_16432e86d97009113cb2aa7fd4ee59df8d570202', //live public key
    email: email,
    amount: "100000",
    currency: "NGN",
    //split_code: "SPL_OVrykLLxU4",
    split_code: "SPL_ZecNHCnDbi", //live split key
    ref: "DIRIBOOST_" + Math.floor((Math.random() * 1000000000) + 1),
    metadata: {
      firstname: fname,
      lastname: lname,
      custom_fields: [
        {
          display_name: "Mobile Number",
          variable_name: "mobile_number",
          value: phone
        },
        {
          display_name: "Full Name",
          variable_name: "full_name",
          value: fname + " " + lname
        }
      ]
    },
    callback: function (response) {
      alert('successfully registered with transaction ref: ' + response.reference);
      $('form').submit();
    },
    onClose: function () {
      alert('Transaction Terminated');
      //$('form').submit();
    }
  });
  handler.openIframe();
});

  // $(".submit").click(function(){
  // 	return false;
  // })
