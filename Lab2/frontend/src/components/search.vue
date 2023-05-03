<script setup lang="ts">
import { ElMessage, ElUpload, ElButton, ElDialog } from "element-plus";
import { Search, UploadFilled,Loading } from "@element-plus/icons-vue";
import { ref } from "vue";
import axios from "axios";

const uploadUrl = ref(void (0));
const image = new FormData();
const imageUrl = ref("");
const uploaded = ref(false);
const searching = ref(false);
const results=ref([]);
const base_url="http://127.0.0.1:5000/image?path=";
const result_base='static/result/'
const handleError = (err: any) => {
  console.error(err);
  ElMessage.error("Server failed");
};

const beforeUpload = (file: any) => {
  const isImage = file.type.includes("image");
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isImage) {
    ElMessage.error("请上传图片文件");
    return false;
  }
  if (!isLt2M) {
    ElMessage.error("请上传小于 2MB 的图片");
    return false;
  }
  image.append('file', file);
  uploaded.value = true;
  console.log("add",image.has('file'));
  return false;
};

const imgPreview = (file: any) => {
  imageUrl.value = URL.createObjectURL(file.raw);
};

const imgDel = () => {
  image.delete('file');
  console.log("del",image.has('file'));
  imageUrl.value = '';
  uploaded.value = false;
};

const imgSearch = () => {
  if (!uploaded.value) {
    ElMessage.error("Please upload an image");
    return false;
  }
  results.value=[];
  searching.value = true;
  console.log("search",image.has('file'));
  let config = {
    method: 'post',
    url: "/imgUpload",
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: image
  }
  console.log(config);
  axios(config).then(
    (response) => {
      // console.log(response);
      searching.value = false;
      for(const key in response.data){
        results.value.push(base_url+result_base+response.data[key]);
      }
      // console.log(results.value);
    }
  ).catch(
    (error) => {
      searching.value = false;
      console.log(error);
      handleError(error);
    });
};

const imgFavorite=(path:string)=>{
  const imgname=path.split('/').pop();
  let config={
    method:'post',
    url:'/favorite',
    params:{
      path:imgname
    }
  };
  axios(config).then(
    (response)=>{
      if(response.data.code === 400){
        ElMessage.error(response.data.msg);
      }
      else{
        ElMessage.success('Added to Favorite Successfully');
      }
    }
  ).catch(
    (error)=>{
      console.log(error);
      handleError(error);
    }
  )
};

</script>

<template>
  <div class="image-input">
    <el-upload :show-file-list=false class="drag" list-type="picture-card" :disabled="uploaded" :drag=true
      :action="uploadUrl" :on-error="handleError" :before-upload="beforeUpload" :on-change="imgPreview">
      <div class="before-upload" v-show="!imageUrl">
        <el-icon class="el-icon-upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
      </div>
      <div class="preview" v-show="imageUrl">
        <el-image :src="imageUrl" :preview-src-list="[imageUrl]" class="el-upload-preview-image" />
        <el-button size="small" type="warning" round @click="imgDel">Delete</el-button>
      </div>
    </el-upload>
    <div class="mb-4">
      <el-button type="primary" :icon="Search" size="large" round @click="imgSearch">Search</el-button>
    </div>
  </div>
  <div class="searching" v-if="searching">
      <el-icon class="is-loading"><Loading/>
      </el-icon>
      <span class="search-tip">Searching...</span>
  </div>
  <div class="result" v-if="results.length>0">
    <h2>{{ results.length }} Results Found</h2>
    <el-row>
      <el-col :span="8" v-for="(item,index) in results" :key="index" style="justify-content: center; display: flex; flex-wrap: wrap;">
        <el-card class="rcard" shadow="hover" style="margin: 10px 10px; width: 250px; text-align: center;">
          <el-image :src="item" class="image" :preview-src-list="[item]"/>
          <div style="padding: 14px; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
            <span>Image {{ index+1 }}</span>
            <div class="bottom">
              <el-button type="primary" @click="imgFavorite(item)">Add Favorite</el-button>
            </div>
          </div>
        </el-card>
        </el-col>
    </el-row>
  </div>
</template>

<style>
.ep-button {
  margin: 4px;
}

.ep-upload input {
  display: none !important;
}

.ep-card__body{
  padding: 0 0 !important;
}

.drag {
  width: 660px;
  height: 300px;
  border: 2px dashed;
  border-color: #a3a3a3;
  border-radius: 5px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  justify-items: center;
  align-items: center;
  flex-wrap: wrap;
}

.img-input{
  display:block;
}

.preview {
  height: 200px;
  display: flex;
  justify-items: center;
  align-items: center;
}

.el-upload-preview-image {
  width: 100%;
  height: 100%;
}

.search-tip{
  font-size: 15px;
  font-weight: bold;
  margin-left: 10px;
}

.bottom{
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image{
  margin:0 0;
  width:100%;
  height:300px;
  object-fit: cover;
}
</style>
