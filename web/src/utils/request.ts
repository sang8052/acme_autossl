/*
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 11:46:56
 * @Description: 
 */
import axios from 'axios';
import { MessagePlugin } from 'tdesign-vue';
import proxy from '../config/host';
import store from '@/store';
import router from '@/router';

const env = import.meta.env.MODE || 'development';
const API_HOST =  proxy[env].API; 

interface ResponseRcp{
  code:number,
  data:any,
  msg:string | undefined
}

declare module 'axios'{
  interface AxiosResponse extends ResponseRcp {}
}

const instance = axios.create({
  baseURL: API_HOST,
  timeout: 8000,
  withCredentials: true,
});

// eslint-disable-next-line
// @ts-ignore
// axios的retry ts类型有问题
instance.interceptors.retry = 3;

instance.interceptors.request.use((config) => {
  const session_id = window.localStorage.getItem("user_session_id")
  config.headers["X-Session-Id"] = session_id;
  // eslint-disable-next-line
 // @ts-ignore
  config.headers["X-App-Version"] = `Acme_AutoSSL ${  import.meta.env.VITE_APP_VERSION}`;
  return config;
});

instance.interceptors.response.use(
  (response) => {
    if (response.status === 200) {
      if(response.data.code === -403){
        if( window.sessionStorage.getItem("handle_user_unlogin") === null){
          window.sessionStorage.setItem("handle_user_unlogin",response.headers["X-Request-Id"]);
          MessagePlugin.error("会话过期,请重新登录!");
          window.localStorage.removeItem("user_session")
          window.localStorage.removeItem("user_session_id")
          store.dispatch("socketio/close_socket");
          router.push(`/login`);
        }
      }
      else if(response.data.code !== 0) MessagePlugin.error(`错误:${  response.data.msg}`);
      return response.data;
    }
    console.error(`请求出错,url:${response.config.url},status:${response.status}`,response.data);
    MessagePlugin.error(`请求出错,url:${response.config.url},status:${response.status}`)
  },
  (err) => {
    const { config } = err;
    if(err.response){
    
      console.error(`请求出错,url:${err.config.url},status:${err.response.status}`,err.response.data);
      MessagePlugin.error(`请求出错,url:${err.config.url},status:${err.response.status}`)
    }
    else{
      MessagePlugin.error("请求出错,未知异常!")
      if (!config || !config.retry) return Promise.reject(err);
      config.retryCount = config.retryCount || 0;
      if (config.retryCount >= config.retry) {
        return Promise.reject(err);
      }
      config.retryCount += 1;
      const backoff = new Promise((resolve) => {
        setTimeout(() => {
          resolve({});
        }, config.retryDelay || 1);
      });
      return backoff.then(() => instance(config));
    }
    
  },
);

export default instance;
