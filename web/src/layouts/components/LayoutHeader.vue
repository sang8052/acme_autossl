<!--
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-06-17 18:33:08
 * @Description: 
-->
<template>
  <common-header
    v-if="showHeader"
    :showLogo="showHeaderLogo"
    :theme="mode"
    :layout="setting.layout"
    :isFixed="setting.isHeaderFixed"
    :menu="headerMenu"
    :isCompact="setting.isSidebarCompact"
    :maxLevel="setting.splitMenu ? 1 : 3"
  />
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';
import CommonHeader from './Header.vue';

import { SettingType } from '@/interface';

export default Vue.extend({
  name: 'LayoutHeader',
  components: {
    CommonHeader,
  },
 
  computed: {
    ...mapGetters({
      showHeader: 'setting/showHeader',
      showHeaderLogo: 'setting/showHeaderLogo',
      mode: 'setting/mode',
      menuRouters: 'permission/routers',
    }),
    setting(): SettingType {
      return this.$store.state.setting;
    },
    
    headerMenu() {
      let menuShowRouter = [];
      menuShowRouter = this.filterMenuRouter(this.menuRouters);
      return menuShowRouter;
    },
  },
  methods:{
    filterMenuRouter(routelist){
      const filterRouters = []
      routelist.forEach((item)=>{
        if(item.showMenu !== 'hide'){
          if(item.showMenu === 'item') filterRouters.push(item);
          if(item.children){
            const childRouters = this.filterMenuRouter( item.children);
            childRouters.forEach((child_item)=>filterRouters.push(child_item)) 
          }
        }
      })
      return filterRouters;
    }
  }
});
</script>
