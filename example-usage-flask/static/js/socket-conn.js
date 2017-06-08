$(document).ready(function() {
  $('.insert1').fadeIn();
  $('.insert2').fadeIn();

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {'reconnection': true,
    'reconnectionDelay': 1000,
    'reconnectionDelayMax' : 5000,
    'reconnectionAttempts': 5 });

  // On connection
  socket.on('connect', function() {
    console.log('Connected');
  });

  // On disconnection
  socket.on('connect', function() {
    console.log('Disconnected');
  });

  socket.on('new_ops', function(ops) {
    var new_op_1 = ops.op1_prime
    var new_op_2 = ops.op2_prime

    $('.log1').append("<b>OP1</b> ", ops.op1, "<br>")
    $('.log1').append("<b>OP1-PRIME</b> ", new_op_1, "<br><br>");
    $('.log2').append("<b>OP2</b> ", ops.op2, "<br>")
    $('.log2').append("<b>OP2-PRIME</b> ", new_op_2, "<br><br>");
  });

  socket.on('apply_original', function(ops) {
    var op1_string = ops.op1_string
    var op1_index = ops.op1_index

    var op2_string = ops.op2_string
    var op2_index = ops.op2_index

    quill.insertText(op1_index, op1_string);
    quill2.insertText(op2_index, op2_string);
  });

  socket.on('apply_transformed', function(ops) {
    var op1_string = ops.op1_string
    var op1_index = ops.op1_index

    var op2_string = ops.op2_string
    var op2_index = ops.op2_index

    quill2.insertText(op1_index, op1_string);
    quill.insertText(op2_index, op2_string);

  });


  $('.op1').on('change', function() {
    if(this.value == "insert-one") {
      $('.insert1').fadeIn();
      $('.delete1').fadeOut();
    }

    if(this.value == "delete-one") {
      $('.insert1').fadeOut();
      $('.delete1').fadeIn();
    }
  })

  $('.op2').on('change', function() {
    if(this.value == "insert-two") {
      $('.insert2').fadeIn();
      $('.delete2').fadeOut();
    }

    if(this.value == "delete-two") {
      $('.insert2').fadeOut();
      $('.delete2').fadeIn();
    }
  })

  $('.transform-button').click(function(){
      var op1_val1 = null
      var op1_val2 = null
      var op2_val1 = null
      var op2_val2 = null
      if($('.op1').val() == "insert-one"){
        console.log('OP1-insert')
        op1_val1 = $('.string-index-1').val();
        op1_val2 = $('.string-1').val();
        op1_type = "Insert"
      }
      if($('.op1').val() == "delete-one"){
        console.log('OP1-delete')
        op1_val1 = $('.delete-index-1').val();
        op1_val2 = $('.range-1').val();
        op1_type = "Delete"
      }
      if($('.op2').val() == "insert-two"){
        console.log('OP2-insert')
        op2_val1 = $('.string-index-2').val();
        op2_val2 = $('.string-2').val();
        op2_type = "Insert"
      }
      if($('.op2').val() == "delete-two"){
        console.log('OP2-delete')
        op2_val1 = $('.delete-index-2').val();
        op2_val2 = $('.range-2').val();
        op2_type = "Delete"
      }

      console.log(op1_val1);
      console.log(op1_val2);

      console.log(op2_val1);
      console.log(op2_val2);

      socket.emit('transform', {op1_index: op1_val1, op1_string: op1_val2, op1_type: op1_type, op2_index: op2_val1, op2_string: op2_val2, op2_type: op2_type})
  });
});
