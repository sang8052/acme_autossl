/*
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 07:43:27
 * @Description: 
 */
import {  Setting1Icon,LockOnIcon,EarthIcon,Certificate1Icon,UserVipIcon} from 'tdesign-icons-vue';

import Layout from '@/layouts/index.vue';

export default [
  {
    path: '/admin',
    component: Layout,
    redirect: '/admin/cert',
    name: 'admin',
    showMenu: 'parent',
    children: [
      {
        path: '/admin/cert',
        name: 'cert',
        showMenu: 'item',
        component: () => import('@/pages/cert/index.vue'),
        meta: { title: '证书管理',icon: Certificate1Icon },
      },
      {
        path: '/admin/domain',
        name: 'domain',
        showMenu: 'item',
        component: () => import('@/pages/domain/index.vue'),
        meta: { title: '域名管理',icon: EarthIcon },
      },
     
      {
        path: '/admin/dnsapi',
        name: 'dnsapi',
        showMenu: 'item',
        component: () => import('@/pages/dnsapi/index.vue'),
        meta: { title: 'DNS 秘钥管理',icon: LockOnIcon },
      },
      {
        path: '/admin/setting',
        name: 'setting',
        showMenu: 'item',
        component: () => import('@/pages/setting/index.vue'),
        meta: { title: '系统配置',icon: Setting1Icon },
      },
      {
        path: '/admin/user',
        name: 'user',
        showMenu: 'item',
        component: () => import('@/pages/user/index.vue'),
        meta: { title: '个人配置',icon: UserVipIcon },
      },
    ],
  }
];
