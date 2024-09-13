<template>
    <div>
        <t-card class="list-card-container" bordered style="height: 780px">
          <t-row justify="space-between">
            <t-col :span="8">
              <div style="width:100%">
                <t-select clearable  :onChange="load_domain_list" v-model="search.key_id" :options="dns_api" placeholder="请选择API秘钥" style="width: 250px; float: left"/>
                <t-input   placeholder="请输入搜索关键字" :onChange="load_domain_list"  v-model="search.keyword" style="width: 250px;float: left;margin-left: 16px;"  clearable  @clear="item_keyword = ''">
                  <template #suffixIcon>
                    <search-icon :style="{ cursor: 'pointer' }" />
                   </template>
                </t-input>
              </div>
              
             
            </t-col>
            <t-col :span="4">
              <t-button
             
                style="float: right; margin-top: 4px"
                @click="on_create_domain()"
                type="button"
              >
                <add-icon slot="icon" /> 新增域名
              </t-button>
            </t-col>
          </t-row>
    
          <div class="table-container" style="height: 666px;margin-top: 16px;">
            <t-table rowKey="id" :columns="columns" :data="data" :loading="data_loading" >
              <template #action="{ row }">
                <t-link  theme="primary" @click="on_detail(row,'view')">详情</t-link>
                <t-link  theme="danger" @click="on_detail(row,'delete')">删除</t-link>
              </template>
            </t-table>
          </div>
          <t-pagination
            :showPageSize="false"
            :total="page_total"
            :defaultPageSize="page_size"
            :defaultCurrent="page_num"
            @change="on_pagination_change"
          />
        </t-card>
        <t-dialog
            :visible.sync="display_detail"
            :header="header_title"
            top="48px"
            width="720px"
        >
         <t-form style="margin-top: 16px" :data="domain_detail" labelWidth="150px" ref="DomainDetail" :rules="form_rules" >
            <t-form-item label="根域名" name="domain">
                <t-input v-model="domain_detail.domain"  placeholder="请输入根域名" :readonly="dialog_type == 'view'" />
            </t-form-item>

            <t-form-item label="API秘钥" name="key_id">
                <t-select clearable v-model="domain_detail.key_id" :options="dns_api" placeholder="请选择API秘钥"/>
            </t-form-item>
        </t-form>
        <div slot="footer" style="margin-top: -16px;">
            <t-button type="button" theme="primary" :loading="btn_loading"   @click="on_submit()" v-if="dialog_type == 'create'">新增</t-button>
            <t-button type="button" theme="default" :loading="btn_loading"  @click="on_close()"   v-if="dialog_type == 'create'" >取消</t-button>
        </div>
        </t-dialog>
    </div>
</template>
<script>
import {domain_data_query,domain_data_detele,dnsapi_data_query,domain_data_create} from '@/api'
import { AddIcon,SearchIcon} from 'tdesign-icons-vue';

export default{
  components:{AddIcon,SearchIcon},

  data(){
    return {  
      page_num:1,
      page_size:10,
      page_total:0,
      search:{keyword:"",key_id:""},
      columns:[
        { colKey: 'domain', title: '根域名', width: 250, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'key_name', title: '秘钥名称', width: 150, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'key_type', title: '秘钥类型', width: 150, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'action', title: '操作', align: 'left', fixed: 'right', width: 300 },
      ],
      data:[],
      data_loading:false,
      display_detail:false,
      header_title:"",
      dialog_type:"",
      btn_loading:false,
      domain_detail:{},
      dns_api:[],
      form_rules:{
        key_id: [{ required: true, message: '请选择API秘钥', type: 'error' }],
        domain: [{ required: true, message: '根域名必填', type: 'error' }],  
      }
    }
  },
  created(){
    this.load_dnsapi_list();
    this.load_domain_list();
  },
  methods:{
    async load_dnsapi_list(){
      const res = await dnsapi_data_query({page_num:1,page_size:999});
      this.dns_api = [];
      res.data.data.forEach((item)=>{
        const option = {"label":item.key_name,"value":item.id};
        this.dns_api.push(option);
      })
    },
    async load_domain_list(){
      this.data_loading = true;
      const querys = {keyword:this.search.keyword,page_num:this.page_num,page_size:this.page_size,key_id:this.search.key_id};
      const res = await domain_data_query(querys)
      this.data = res.data.data;
      this.data_loading = false;
      this.page_num = res.data.page_num;
      this.page_size =res.data.page_size;
      this.page_total = res.data.total ;
    },
    on_create_domain(){
      this.$refs.DomainDetail.reset();
      this.header_title = '新建域名';
      this.dialog_type = 'create';
      this.display_detail = true;
      this.load_dnsapi_list();
    },
    on_pagination_change(page){
      this.page_num = page.current;
      this.page_size = page.pageSize;
      this.load_domain_list();
    },
    async on_detail(row,type){
      if(type === 'delete'){
        const dialog = this.$dialog.confirm({
          header: '提示',
          body: '此操作不可逆,确认执行?',
          confirmBtn: '确定',
          cancelBtn: '取消',
          onConfirm: async () => {
            const res = await domain_data_detele(row.id);
            if (res.code === 0) {
              this.$message.success('删除域名信息成功!');
              this.on_close();
            }
            dialog.hide();
          },
          onClose: async () => {
            dialog.hide();
          },
        });
      }
      else{
        this.domain_detail = row;
        this.display_detail = true;
        this.dialog_type = type;
        this.header_title = '查看域名信息';
      }
    },
    on_close(){
      this.load_domain_list();
      this.display_detail = false;
    },
    async on_submit(){
      const validate = await this.$refs.DomainDetail.validate();
      if(typeof(validate) === typeof(true)){
        
        const payload =  {...this.domain_detail};
        this.btn_loading =true;
        const  res = await domain_data_create(payload);
        if(res.code === 0) this.$message.success(res.msg);
        this.btn_loading = false;
        this.on_close();
      
      }
    }
  }
}
</script>