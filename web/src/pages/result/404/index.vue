<!--
 * @Author: SudemQaQ
 * @Date: 2024-07-23 15:05:58
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-26 22:55:33
 * @Description: 
-->
<template>
  <result title="404 Not Found" tip="抱歉，您访问的页面不存在" type="404">
    <t-button @click="() => $router.push('/admin')">返回首页</t-button>
  </result>
</template>

<script>
import result from '@/components/result/index.vue';

export default {
  name: 'Result404',
  components: { result },
};
</script>
