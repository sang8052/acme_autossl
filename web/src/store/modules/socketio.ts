// import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";
import { io } from 'socket.io-client';

import log from '@/utils/log';
import proxy from '@/config/host';

const state = {
  client: null,
  client_heart: null,
};

const mutations = {
  set_client: (state, client) => {
    state.client = client;
  },
  set_heart: (state, heart) => {
    state.heart = heart;
  },

  clear_heart: (state) => {
    if (state.heart) setInterval(state.heart);
    state.heart = null;
  },
};

const getters = {
  client: (state) => state.client,
};

const actions = {
  // 关闭socket 会话
  async close_socket({ commit }) {
    if (state.client) {
      state.client.offAny();
      state.client.disconnect();
      commit('client', null);
      state.client = null;
      log.info('[SocketIo]会话已终止');
    }
  },
  async init_socket({ commit }) {
    const env = import.meta.env.MODE || 'development';
    const WSS_HOST = proxy[env].WSS;
    const session_id = window.localStorage.getItem('user_session_id');
    let websocket_url = '';
    if (!state.client) {
      if (env !== 'development') {
        if (window.location.protocol === 'https:') websocket_url = `wss://${  window.location.host  }/socket_io`;
        else websocket_url = `ws://${  window.location.host  }/socket_io`;
      } 
      else websocket_url = `${WSS_HOST}/socket_io`;

      console.log(`socket_io:${  websocket_url}`);
      const client = io(websocket_url, {
        autoConnect: false,
        ackTimeout: 10000,
        retries: 3,
        extraHeaders: {
          'X-Session-Id': session_id,
          'X-App-Version': `Acme_AutoSSL ${import.meta.env.VITE_APP_VERSION}`,
        },
      });
      commit('set_client', client);
      client.connect();
      client.on('connect', () => {
        const client_heart = setInterval(() => {
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-expect-error
          const timestamp = Date.parse(new Date());
          client.emit('heart', { timestamp, session_id });
        }, 30 * 1000);
        log.success('[SocketIo]会话连接成功!');
        commit('set_heart', client_heart);
      });

      client.on('auth success', (client) => {
        log.success(`[SocketIo]服务器认证成功!当前客户端信息:${client}`);
      });

      client.on('disconnect', (reason) => {
        log.warning(`[SocketIo]客户端断开了连接,原因:${reason}`);
        commit('clear_heart');
        // 释放会话
        if (reason === 'io server disconnect' || reason === 'io client disconnect') {
          // eslint-disable-next-line no-empty
          try {
            state.client.disconnect();
          } catch (err) {}
          commit('client', null);
        }
      });
    } else log.warning('[SocketIo]会话已经被初始化...');
  },
};

export default {
  namespaced: true,
  mutations,
  actions,
  state,
  getters,
};
