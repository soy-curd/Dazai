
var BookRender = React.createClass({
  submitMarkdown: function(markdown_obj) {
    var submit_data = JSON.stringify(markdown_obj);
    
    $.ajax({
      url: this.props.url,
      contentType: 'application/json',
      dataType: 'json',
      type: 'POST',
      data: submit_data,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  
  getInitialState: function(){
    return {data: {results: {pdf_filename: ""}}}
  },
  componentDidMount: function() {
    setInterval(10);
  },
  
  render: function() {
    return (
      <div className="bookRender">
        <p><div ref="pdflink"></div></p>
        値を入力してください。
        {this.componentDidMount()}
        <MarkdownForm onTextSubmit={this.submitMarkdown} />
        <PdfLink pdfname={this.state.data.results.pdf_filename} />
      </div>
    );
  }
});

var MarkdownForm = React.createClass({
  handleSubmit: function(e) {
    e.preventDefault();
    var booktitle = React.findDOMNode(this.refs.booktitle).value.trim();
    var aut = React.findDOMNode(this.refs.aut).value.trim();
    var pbl = React.findDOMNode(this.refs.pbl).value.trim();
    var prt = React.findDOMNode(this.refs.prt).value.trim();
    var contact = React.findDOMNode(this.refs.contact).value.trim();
    var prt_url = React.findDOMNode(this.refs.prt_url).value.trim();
    var rights = React.findDOMNode(this.refs.rights).value.trim();
    var preface = React.findDOMNode(this.refs.preface).value.trim();
    var markdown = React.findDOMNode(this.refs.markdown).value.trim();
    
    // submitMarkdownを実行
    this.props.onTextSubmit({markdown: markdown,
                            booktitle: booktitle,
                            aut: aut,
                            pbl: pbl,
                            prt: prt,
                            contact: contact,
                            prt_url: prt_url,
                            rights: rights,
                            preface: preface,
                            dummy: "dummy string."})
    React.findDOMNode(this.refs.booktitle).value = booktitle;
    React.findDOMNode(this.refs.aut).value = aut;
    React.findDOMNode(this.refs.pbl).value = pbl;
    React.findDOMNode(this.refs.prt).value = prt;
    React.findDOMNode(this.refs.contact).value = contact;
    React.findDOMNode(this.refs.prt_url).value = prt_url;
    React.findDOMNode(this.refs.rights).value = rights;
    React.findDOMNode(this.refs.preface).value = preface;
    React.findDOMNode(this.refs.markdown).value = markdown;
    React.findDOMNode(this.refs.pdflink).value = "ダウンロード";

    return;
  },
  
  render: function() {
    return (
      // submit時に実行
      <form class="form-horizontal" className="markdownForm" onSubmit={this.handleSubmit}>
        <div class="form-group">
          <input class="form-control" name="booktitle" placeholder="書名" ref="booktitle"></input>
        </div>
        <div class="form-group">
          <input class="form-control" name="aut" placeholder="著者名" ref="aut"></input>
        </div>
        <div class="form-group">
          <input class="form-control" name="pbl" placeholder="出版社" ref="pbl"></input>
        </div>
        <div class="form-group">
          <input class="form-control" name="prt" placeholder="印刷所" ref="prt"></input>
        </div>
        <div class="form-group">
          <input class="form-control" name="contact" placeholder="メールアドレス" ref="contact"></input>
        </div>
        <div class="form-group">
          <input name="prt_url" class="form-control" placeholder="サイトURL" ref="prt_url"></input>
        </div>
        <div class="form-group">
          <input name="rights" class="form-control" placeholder="copyright" ref="rights"></input>
        </div>
        <div class="form-group">
          <textarea name="preface" id="inp_pre" cols="50" rows="20"      placeholder="緒言マークダウン" ref="preface" ></textarea>
        </div>
        <div class="form-group">
          <textarea name="input_text" id="inp" cols="50" rows="20"      placeholder="記事マークダウン" ref="markdown" ></textarea>
        </div>

        <button type="submit" class="btn btn-default" id="button">送信</button>       
      </form>
    );
  }
})

var PdfLink = React.createClass({
  render: function() {
    if (this.props.pdfname) {
      var linkString = "ダウンロード";
    } else {
      var linkString = "";
    };
    
    return (
      <div>
        <a href={ "/static/pdf/" + this.props.pdfname } target="_blank" ref="pdflink">
          {linkString}
        </a>  
      </div>
    )
  }
})

React.render(
  <BookRender />,
  document.getElementById('content')
);
