(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{100:function(e,t){function n(e){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}n.keys=function(){return[]},n.resolve=n,e.exports=n,n.id=100},110:function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a),c=n(54),l=n.n(c),r=(n(65),n(2)),i=n(3),u=n(7),s=n(5),p=n(6),m=(n(35),o.a.Component,n(32)),h=n(33),d=["Select an Option","First Option","Second Option","Third Option"],f=function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(u.a)(this,Object(s.a)(t).call(this,e))).getInputValue=function(e){n.props.parentCallback(e.target.value)},n.state={value:"Select an Option"},n}return Object(p.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return o.a.createElement("div",{className:"form-group fontFamiliesSection"},o.a.createElement("label",{htmlFor:"fontFamilies"},"Font Family"),o.a.createElement("select",{value:this.state.value,onChange:this.getInputValue,className:"form-control"},d.map(function(e){return o.a.createElement("option",{value:e,key:e},e)})))}}]),t}(o.a.Component),b=n(25),g=n.n(b),C=function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(u.a)(this,Object(s.a)(t).call(this,e))).getInputValue=function(e){n.props.parentCallback(e.target.value)},n}return Object(p.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return o.a.createElement("div",{className:"form-group fontFamiliesSection"},o.a.createElement("label",{htmlFor:"fontFamilies"},"Font Size"),o.a.createElement("input",{type:"number",title:"Rate",id:"lineSpace",className:"form-control",min:"1",step:"1",max:"400",onChange:this.getInputValue}),o.a.createElement("input",{type:"number",id:"tentacles",name:"tentacles",min:"1",max:"400",step:1,onChange:this.getInputValue}),o.a.createElement(g.a,{className:"form-control",value:12,min:0,max:400,step:1,precision:0,onChange:this.getInputValue}))}}]),t}(o.a.Component),k=function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(u.a)(this,Object(s.a)(t).call(this,e))).getInputValue=function(e){n.props.parentCallback(e.target.value)},n.state={LineSpace:""},n}return Object(p.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return o.a.createElement("div",{className:"form-group fontFamiliesSection"},o.a.createElement("label",{htmlFor:"lineSpace"},"Line Spacing"),o.a.createElement("input",{type:"number",title:"Rate",id:"lineSpace",className:"form-control",min:"1.0",step:"0.05",max:"2.0",onChange:this.getInputValue}))}}]),t}(o.a.Component),v=n(12),O=n.n(v),w=n(19),E=(o.a.Component,n(99),n(55)),j=n(8),y=function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(u.a)(this,Object(s.a)(t).call(this,e))).getInputValue=function(e){n.props.parentCallback(e.target.value)},n}return Object(p.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return o.a.createElement("div",{className:"form-group wordCountSection"},o.a.createElement("label",{htmlFor:"",className:"wordCountTitle"},"Word Count Threshold"),o.a.createElement("br",null),o.a.createElement("label",{htmlFor:"",className:"wordCount"},"How many total words you want to write"),o.a.createElement("input",{type:"number",title:"Rate",id:"wordCount",className:"form-control",min:"0",step:"1",onChange:this.getInputValue}))}}]),t}(o.a.Component),N=function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(u.a)(this,Object(s.a)(t).call(this,e))).getInputValue=function(e){n.props.parentCallback(e.target.value)},n}return Object(p.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return o.a.createElement("div",{className:"form-group pageCountSection"},o.a.createElement("label",{htmlFor:"",className:"pageCountTitle"},"Page Count Threshold"),o.a.createElement("br",null),o.a.createElement("label",{htmlFor:"",className:"pageCount"},"How many total pages you want to write"),o.a.createElement("input",{type:"number",title:"Rate",id:"pageCount",className:"form-control",min:"0",step:"1",onChange:this.getInputValue}))}}]),t}(o.a.Component),S=n(34),I=n.n(S),R=(n(103),n(24)),F=n.n(R);window.Swal=F.a;Object({NODE_ENV:"production",PUBLIC_URL:"."}).PORT;var T=function(e){function t(e){var n;return Object(r.a)(this,t),(n=Object(u.a)(this,Object(s.a)(t).call(this,e))).sendThr=function(){console.log("post"),setInterval(function(){n.checkRoadblock()},5e3),setInterval(function(){n.checkCompletion()},5e3),setInterval(function(){n.sendML()},3e5),O.a.post("https://cruise-extension.herokuapp.com:80/api/thr/",{wordCount:n.state.wordCount,pageCount:n.state.pageCount}).then(function(e){console.log(e),console.log(e.data.wordcount),e.ok?F.a.fire({title:"We expect you to take "+(e.data.wordcount/60).toFixed(2)+" minutes",text:"",icon:"OK",confirmButtonColor:"#3085d6",cancelButtonColor:"#d33",confirmButtonText:"OK"}):F.a.fire("Unsuccessful","Unable to delete selected user. Please contact administrator.","error")})},n.sendML=function(){O.a.get("https://cruise-extension.herokuapp.com/api/ml",{port:80})},n.handleCallbackOne=function(e){n.setState(Object(j.a)({},n.state,{wordCount:e}))},n.handleCallbackTwo=function(e){console.log(e),n.setState(Object(j.a)({},n.state,{pageCount:e}))},n.state={isRoadblock:!1,isCompletion:!1,wordCount:0,pageCount:0,open:!1,title:""},n}return Object(p.a)(t,e),Object(i.a)(t,[{key:"showRoadblockNotifications",value:function(){console.log(this.n.supported()),this.n.supported(),this.n.show()}},{key:"showCompNotifications",value:function(){console.log(this.a.supported()),this.a.supported(),this.a.show()}},{key:"handleRoadClick",value:function(e){this.n.close(e.target.tag)}},{key:"handleCompClick",value:function(e){this.a.close(e.target.tag)}},{key:"checkRoadblock",value:function(){var e=this;O.a.get("https://cruise-extension.herokuapp.com/api/roadblock",{port:80}).then(function(t){"True"==t.data[0]&&(console.log("roadblock notifs"),e.state.isRoadblock=!0,1==e.state.isRoadblock&&F.a.fire({title:"You have approached a roadblock!",text:"",icon:"OK",confirmButtonColor:"#3085d6",cancelButtonColor:"#d33",confirmButtonText:"OK",iconHtml:'<img src="/src/components/sad_whale.png">'}),e.state.isRoadblock=!1)}).catch(function(e){return console.log("Show error notification! "+e),Promise.reject(e)})}},{key:"checkCompletion",value:function(){var e=this;O.a.get("https://cruise-extension.herokuapp.com/api/completion",{port:80}).then(function(t){"True"==t.data[0]&&(e.state.notRun=!0,console.log("completion notifs"),e.state.isCompletion=!0,1==e.state.isCompletion&&F.a.fire({title:"You have completed your goal!",text:"",icon:"OK",confirmButtonColor:"#3085d6",cancelButtonColor:"#d33",confirmButtonText:"OK",iconHtml:'<img src="/src/components/happy_whale.png">'}),e.state.isCompletion=!1)}).catch(function(e){return console.log("Show error notification! "+e),Promise.reject(e)})}},{key:"handleButtonClick",value:function(){if(!this.state.ignore){var e=Date.now(),t="React-Web-Notification"+e,n={tag:e,body:"Hello"+new Date,lang:"en",dir:"ltr"};this.setState({title:t,options:n})}}},{key:"handleButtonClick2",value:function(){this.props.swRegistration.getNotifications({}).then(function(e){console.log(e)})}},{key:"render",value:function(){var e=this;return o.a.createElement("div",{className:"thresholdsList"},o.a.createElement(I.a,{onRef:function(t){return e.n=t},title:"You have approached a roadblock!",body:"You have approached a roadblock!",tag:"roadblock",timeout:"2000",onClick:function(t){return e.handleRoadClick(t)}}),o.a.createElement(I.a,{onRef:function(t){return e.a=t},title:"You have completed your goal!",body:"You have completed your goal!",tag:"completion",timeout:"2000",onClick:function(t){return e.handleCompClick(t)}}),o.a.createElement("div",null),o.a.createElement("div",{id:"thresholdsList"},o.a.createElement(y,{parentCallback:this.handleCallbackOne}),o.a.createElement(N,{parentCallback:this.handleCallbackTwo}),o.a.createElement("button",{className:"btn btn-success",onClick:this.sendThr},"submit")))}}]),t}(o.a.Component);o.a.Component,n(108);var x=function(){return Object(E.a)({apiKey:"AIzaSyBbqaOCwIZocSgjT1-Z1JAlWlr5obER7Z0",authDomain:"cruise-e8304.firebaseapp.com",projectId:"cruise-e8304",storageBucket:"cruise-e8304.appspot.com",messagingSenderId:"665446251636",appId:"1:665446251636:web:4bb27580e5f968c112a521",measurementId:"G-4B33G21KR0"}),o.a.createElement("div",{className:"App"},o.a.createElement(T,null))},B=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,112)).then(function(t){var n=t.getCLS,a=t.getFID,o=t.getFCP,c=t.getLCP,l=t.getTTFB;n(e),a(e),o(e),c(e),l(e)})};l.a.createRoot(document.getElementById("root")).render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(x,null))),B()},58:function(e,t,n){e.exports=n(110)},65:function(e,t,n){}},[[58,1,2]]]);
//# sourceMappingURL=main.2e8372de.chunk.js.map