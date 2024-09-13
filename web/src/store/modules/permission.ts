/*
 * @Author: SudemQaQ
 * @Date: 2024-07-23 15:05:58
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 11:08:56
 * @Description: 
 */
import { resetRouter,asyncRouterList } from '@/router';



const state = {
  whiteListRouters: ['/login'],
  routers: [],
};

const mutations = {
  setRouters: (state, routers) => {
    state.routers = routers;
  },
};

const getters = {
  routers: (state) => state.routers,
  whiteListRouters: (state) => state.whiteListRouters,
};

const actions = {
  async initRoutes({ commit }) {
    commit('setRouters', asyncRouterList);
  },
  async restore({ commit }) {
    resetRouter();
    commit('setRouters', []);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
