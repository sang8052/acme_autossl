/*
 * @Author: SudemQaQ
 * @Date: 2024-07-23 15:05:57
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-09-13 12:44:07
 * @Description: 
 */

import Vue from 'vue';
import VueRouter from 'vue-router';
import { sync } from 'vuex-router-sync';
import TDesign from 'tdesign-vue';
import VueClipboard from 'vue-clipboard2';
import axiosInstance from '@/utils/request';
import App from './App.vue';
import router from './router';
import zhConfig from 'tdesign-vue/es/locale/zh_CN';

import 'tdesign-vue/es/style/index.css';
import '@/style/index.less';

import './permission';
import store from './store';
import CKEditor from '@ckeditor/ckeditor5-vue2';


Vue.use(VueRouter);
Vue.use( TDesign );
Vue.use(VueClipboard);
Vue.use( CKEditor );

Vue.component('t-page-header');



Vue.prototype.$request = axiosInstance;

const originPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originPush.call(this, location).catch((err) => err);
};

const originReplace = VueRouter.prototype.replace;
VueRouter.prototype.replace = function replace(location) {
  return originReplace.call(this, location).catch((err) => err);
};

Vue.config.productionTip = false;
sync(store, router);

console.info(`%c [Acme_AutoSSL]:${   import.meta.env.VITE_APP_VERSION}`,"color:red;");

new Vue({
  router,
  store,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  render: (h) => (
    <div>
      {/* 可以通过config-provider提供全局（多语言、全局属性）配置，如 
      <t-config-provider globalConfig={enConfig}> */}
      <t-config-provider globalConfig={zhConfig}>
        <App />
      </t-config-provider>
    </div>
  ),
  created(){
    // 关闭socket 会话
    this.$store.dispatch("socketio/close_socket")
    // 初始化socketio 连接
    this.$store.dispatch("socketio/init_socket")
  }
}).$mount('#app');


