(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{da3b:function(t,e,a){"use strict";a.r(e);var s=a("e4fd"),i=a("fe17"),n=Object(s.defineComponent)({name:"WiFi",components:{WifiButton:i.a},setup:()=>({automatic:Object(s.ref)(!0)})}),c=a("2877"),o=a("9989"),l=a("2bb1"),r=a("9c40"),d=a("f09f"),p=a("a370"),u=a("1c1c"),m=a("66e5"),f=a("4074"),b=a("0170"),w=a("9564"),q=a("27f9"),v=a("714f"),C=a("eebe"),h=a.n(C),y=Object(c.a)(n,function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("q-page",{staticClass:"fit column items-center justify-start content-center q-pa-lg"},[a("div",{staticClass:"full-width row",staticStyle:{"max-width":"320px"}},[a("div",{staticClass:"full-width row q-my-sm"},[a("div",{staticClass:"text-h7"},[t._v("Firmware Update")])]),a("div",{staticClass:"full-width column q-my-sm"},[a("q-markup-table",{attrs:{flat:"",bordered:""}},[a("thead",[a("tr",[a("th",{staticClass:"text-left"},[t._v("Current Version")]),a("th",{staticClass:"text-right"},[t._v("Available Update")])])]),a("tbody",[a("tr",[a("td",{staticClass:"text-left"},[t._v("HYPNOTIK 1.0.1")]),a("td",{staticClass:"text-right"},[t._v("HYPNOTIK 1.2.0")])])])])],1),a("div",{staticClass:"full-width column q-my-sm text-center"},[a("div",[t._v("Last checked : 20 Nov, 2020 | 12:19 PM")]),a("q-btn",{attrs:{label:"Check for Updates",icon:"updates",stack:""}})],1)]),a("div",{staticClass:"full-width column q-my-sm"},[a("q-card",{staticClass:"col-grow"},[a("q-card-section",[a("q-list",[a("q-item",{directives:[{name:"ripple",rawName:"v-ripple"}]},[a("q-item-section",[a("q-item-label",[t._v("Automatic Updates")])],1),a("q-item-section",{attrs:{avatar:""}},[a("q-toggle",{attrs:{size:"xl",dense:"",icon:"done"},model:{value:t.automatic,callback:function(e){t.automatic=e},expression:"automatic"}})],1)],1)],1)],1)],1)],1),a("div",{staticClass:"full-width column q-my-sm"},[a("q-card",{staticClass:"col-grow"},[a("q-card-section",[t._v("\n        Update by File Upload\n      ")]),a("q-card-section",[a("q-input",{attrs:{type:"file"}})],1),a("q-card-section",{staticClass:"text-center"},[a("q-btn",{attrs:{label:"Start Update",icon:"updates"}})],1)],1)],1)])},[],!1,null,null,null);e.default=y.exports,h()(y,"components",{QPage:o.a,QMarkupTable:l.a,QBtn:r.a,QCard:d.a,QCardSection:p.a,QList:u.a,QItem:m.a,QItemSection:f.a,QItemLabel:b.a,QToggle:w.a,QInput:q.a}),h()(y,"directives",{Ripple:v.a})},fe17:function(t,e,a){"use strict";var s=a("e4fd"),i=Object(s.defineComponent)({name:"WifiButton",components:{},props:{network:{type:Object,required:!0},applyingchanges:{type:Boolean,default:!1}},setup(t,{emit:e}){const a=Object(s.ref)("");return{isPwd:Object(s.ref)(!0),password:a,emitConnect:function(){e("connect",a.value)}}}}),n=a("2877"),c=a("66e5"),o=a("4074"),l=a("27f9"),r=a("0016"),d=a("9c40"),p=a("eebe"),u=a.n(p),m=Object(n.a)(i,function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("q-item",{staticClass:"q-mb-sm"},[a("q-item-section",{attrs:{"no-wrap":""}},[a("q-input",{attrs:{hint:"Password",type:t.isPwd?"password":"text"},scopedSlots:t._u([{key:"append",fn:function(){return[a("q-icon",{staticClass:"cursor-pointer",attrs:{name:t.isPwd?"visibility_off":"visibility"},on:{click:function(e){t.isPwd=!t.isPwd}}})]},proxy:!0}]),model:{value:t.password,callback:function(e){t.password=e},expression:"password"}})],1),a("q-item-section",{attrs:{side:"",top:""}},[a("q-btn",{attrs:{flat:"",round:"",color:"primary",icon:"done",loading:t.applyingchanges,disable:t.password.length<=0},on:{click:t.emitConnect}})],1)],1)},[],!1,null,null,null);e.a=m.exports,u()(m,"components",{QItem:c.a,QItemSection:o.a,QInput:l.a,QIcon:r.a,QBtn:d.a})}}]);