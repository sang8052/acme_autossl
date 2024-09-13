/* eslint-disable import/prefer-default-export */
/*
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:45:03
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-09-12 16:19:53
 * @Description: 
 */
import request from '@/utils/request'

export function user_login(data){
  return request({
    url:"/user/login/",
    method:'post',
    data
  })
}

export function user_reg(data){
  return request({
    url:"/user/reg/",
    method:'post',
    data
  })
}

export function user_resetpassword(data){
  return request({
    url:"/user/password/",
    method:'post',
    data
  })
}

export function user_update(data){
  return request({
    url:"/user/",
    method:'post',
    data
  })
}

export function user_session(params){
  return request({
    url:"/user/",
    method:'get',
    params
  })
}


export function dnsapi_system_support(params){
  return request({
    url:"/dnsapi/system/",
    method:'get',
    params
  })
}

export function dnsapi_data_query(params){
  return request({
    url:"/dnsapi/",
    method:'get',
    params
  })
}

export function dnsapi_data_create(data){
  return request({
    url:"/dnsapi/",
    method:'post',
    data
  })
}


export function dnsapi_data_detail(id){
  return request({
    url:`/dnsapi/${  id}/` ,
    method:'get',
  })
}


export function dnsapi_data_update(id,data){
  return request({
    url:`/dnsapi/${  id}/` ,
    method:'post',
    data
  })
}

export function dnsapi_data_delete(id){
  return request({
    url:`/dnsapi/${  id}/` ,
    method:'delete',
  })
}



export function domain_data_query(params){
  return request({
    url:"/domain/",
    method:'get',
    params
  })
}

export function domain_data_create(data){
  return request({
    url:"/domain/",
    method:'post',
    data
  })
}

export function domain_data_detele(id){
  return request({
    url:`/domain/${  id}/` ,
    method:'delete',
  })
}


export function cert_data_query(params){
  return request({
    url:"/cert/",
    method:'get',
    params
  })
}


export function cert_data_detail(id){
  return request({
    url:`/cert/${  id}/` ,
    method:'get',
  })
}


export function cert_data_delete(id){
  return request({
    url:`/cert/${  id}/` ,
    method:'delete',
  })
}


export function cert_data_create(data){
  return request({
    url:`/cert/` ,
    method:'post',
    data
  })
}


export function task_status(id){
  return request({
    url:`/task/${  id}/`  ,
    method:'get',
  })
}


export function config_query(params){
  return request({
    url:`/config/` ,
    method:'get',
    params
  })
}


export function config_detail(item_name){
  return request({
    url:`/config/${  item_name}/`,
    method:'get',
  })
}


export function config_create(data){
  return request({
    url:`/config/` ,
    method:'get',
    data
  })
}


export function config_delete(id){
  return request({
    url:`/config/${  id}/`  ,
    method:'delete',
    
  })
}


export function config_update(id,data){
  return request({
    url:`/config/${  id}/`  ,
    method:'post',
    data
  })
}

export function config_update_list(data){
  return request({
    url:`/config/`  ,
    method:'put',
    data
  })
}