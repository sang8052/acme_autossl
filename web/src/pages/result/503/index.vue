<!--
 * @Author: SudemQaQ
 * @Date: 2024-06-19 22:22:24
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-06-19 22:22:31
 * @Description: 
-->
<template>
    <result title="503 Service Unavailable" tip="抱歉，当前页面正在开发中,暂不可用..." type="503">
      <t-button @click="() => $router.push('/')">返回首页</t-button>
    </result>
  </template>
  
<script>
import result from '@/components/result/index.vue';
  
export default {
  name: 'Result503',
  components: { result },
};
</script>
  