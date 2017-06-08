var toolbarOpt = ['bold', 'italic', 'underline']
var options = {
  debug: 'info',
  placeholder: 'ABC',
  readOnly: true,
  theme: 'bubble',
  modules: {
    toolbar: false
  },
};

var quill = new Quill('#repo1', options);
var quill2 = new Quill('#repo2', options);
