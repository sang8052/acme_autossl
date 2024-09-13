/*
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 09:41:27
 * @Description: 
 */
import VueRouter from 'vue-router';


import baseRouters from './modules/admin';
import componentsRouters from './modules/components';


// 存放动态路由
export const asyncRouterList = [...baseRouters,...componentsRouters];


// 存放固定的路由
const defaultRouterList = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/login/index.vue'),
  },

  {
    path: '/',
    name: 'index',
    redirect:"/admin/cert"
  },
  {
    path: '*',
    redirect: '/result/404',
  },
  ...asyncRouterList
]


const createRouter = () =>
  new VueRouter({
    mode: 'history',
    base: import.meta.env.BASE_URL,
    routes: defaultRouterList,
    scrollBehavior() {
      return { x: 0, y: 0 };
    },
  });

const router = createRouter();

export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher; // reset router
}

export default router;
