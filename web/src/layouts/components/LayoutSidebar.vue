<template>
  <side-nav
    v-if="showSidebar"
    :showLogo="showSidebarLogo"
    :layout="setting.layout"
    :isFixed="setting.isSidebarFixed"
    :menu="sideMenu"
    :theme="mode"
    :isCompact="setting.isSidebarCompact"
    :maxLevel="setting.splitMenu ? 2 : 3"
  />
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';
import SideNav from './SideNav.vue';

import { SettingType } from '@/interface';

export default Vue.extend({
  name: 'LayoutSidebar',
  components: {
    SideNav,
  },
 
  computed: {
    ...mapGetters({
      showSidebar: 'setting/showSidebar',
      showSidebarLogo: 'setting/showSidebarLogo',
      mode: 'setting/mode',
      menuRouters: 'permission/routers',
    }),
    setting(): SettingType {
      return this.$store.state.setting;
    },
    sideMenu() {
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
  },
});
</script>
<style lang="less" scoped></style>
