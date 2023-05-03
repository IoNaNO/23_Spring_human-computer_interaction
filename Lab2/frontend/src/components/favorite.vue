<template>
  <div>
    <h2>{{ favorites.length }} image in Favorites </h2>
    <el-row>
      <el-col :span="8" v-for="(item,index) in favorites" :key="index" style="justify-content: center; display: flex; flex-wrap: wrap;">
        <el-card class="rcard" shadow="hover" style="margin: 10px 10px; width: 250px; text-align: center;">
          <el-image :src="item" class="image" :preview-src-list="[item]"/>
          <div style="padding: 14px; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
            <span>Image {{ index+1 }}</span>
            <div class="bottom">
              <el-button type="warning" @click="imgRemove(item)">Remove Favorite</el-button>
            </div>
          </div>
        </el-card>
        </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import axios from 'axios';
import { ElButton,ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
const favorites=ref([]);
const router=useRouter();
const base_url="http://127.0.0.1:5000/image?path=";
const favorite_base='static/favorite/';

const handleError=(err:any)=>{
  console.error(err);
  ElMessage.error('Server failed');
};

const getFavorites=()=>{
  let config={
    method:'get',
    url:'/favorite'
  };
  axios(config).then(
    (response)=>{
      for(const key in response.data){
        favorites.value.push(base_url+favorite_base+response.data[key]);
      }
    }
  ).catch(
    (err)=>{
      handleError(err);
    }
  )
};
getFavorites();

const imgRemove=(path:string)=>{
  const name=path.split('/').pop();
  let config={
    method:'delete',
    url:'/favorite',
    params:{
      path:name
    }
  };
  axios(config).then(
    (response)=>{
      if(response.data.code === 400){
        ElMessage.error(response.data.msg);
      }
      else{
        ElMessage.success('Removed from Favorite Successfully');
        favorites.value=[];
        getFavorites();
      }
    }
  )
}

</script>

<style>

</style>