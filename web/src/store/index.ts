/*
 * @Author: SudemQaQ
 * @Date: 2024-07-23 15:05:58
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 04:09:00
 * @Description: 
 */
import Vue from 'vue';
import Vuex from 'vuex';
import notification from './modules/notification';
import setting from './modules/setting';
import permission from './modules/permission';
import tabRouter from './modules/tab-router'; // 多标签管理
import socketio from './modules/socketio';

Vue.use(Vuex);

const store = new Vuex.Store({
  strict: import.meta.env.MODE === 'release',
  modules: {
    setting,
    notification,
    permission,
    tabRouter,
    socketio
  },
});

export default store;
