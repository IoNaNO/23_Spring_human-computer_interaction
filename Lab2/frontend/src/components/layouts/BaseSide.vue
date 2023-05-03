<template>
  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
  >
    <el-menu-item index="1" @click="gotoSearch()">
      <el-icon><icon-menu /></el-icon>
      <template #title>Application</template>
    </el-menu-item>
    <el-menu-item index="2" @click="gotoSetting()">
      <el-icon><setting /></el-icon>
      <template #title>Setting</template>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import {
  Location,
  Document,
  Menu as IconMenu,
  Setting,
} from "@element-plus/icons-vue";
const router=useRouter();
const isCollapse = ref(false);
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

const gotoSearch=()=>{
  router.push('/');
};
const gotoSetting=()=>{
  router.push('/settings');
};
</script>

