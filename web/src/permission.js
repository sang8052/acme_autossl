/*
 * @Author: SudemQaQ
 * @Date: 2024-07-23 15:05:57
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 11:11:49
 * @Description: 
 */
import NProgress from 'nprogress'; // progress bar
import 'nprogress/nprogress.css'; // progress bar style

import store from '@/store';
import router from '@/router';

NProgress.configure({ showSpinner: false });


router.beforeEach(async (to, from, next) => {
  NProgress.start();
  const token = window.localStorage.getItem("user_session_id");
  if (token) {
    await store.dispatch('permission/initRoutes');
    next();
  }
  else if(to.path === '/login') {
    next();
  }
  else{
    window.localStorage.removeItem("user_session_id");
    next(`/login`);
    NProgress.done();
  } 
});

router.afterEach(() => {
  NProgress.done();
});
