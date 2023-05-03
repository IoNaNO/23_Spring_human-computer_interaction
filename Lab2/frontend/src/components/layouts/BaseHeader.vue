<script setup lang="ts">
import { toggleDark } from "~/composables";
import { useRouter } from "vue-router";
const router=useRouter();
const gotoSearch=()=>{
  router.push('/')
}
const gotoFavorite=()=>{
  router.push('/favorite')
}
// export default{
//   methods:{
//     gotoSearch(){
//       this.$router.push('/')
//     },
//     gotoFavorite(){
//       this.$router.push('/favorite')
//     }
//   }
// }
</script>

<template>
  <div>
  <el-menu class="el-menu-demo" mode="horizontal" default-active="1">
    <div class="logo-container">
      <img src="/src/assets/search.png" alt="Logo" class="logo" />
    </div>
    <!-- <router-link tag='el-menu-item' index="1" :to="{ name:'search'}">Image Search</router-link> -->

    <el-menu-item index="1" @click="gotoSearch()"> Image Search</el-menu-item>
    <!-- <router-link :to="{ name:'favorite'}" custom v-slot="{navigate}"> -->
    <el-menu-item index="2" @click="gotoFavorite()">Favourite</el-menu-item>
    <!-- </router-link> -->
    <el-menu-item h="full" @click="toggleDark()">
      <button
        class="border-none w-full bg-transparent cursor-pointer"
        style="height: var(--ep-menu-item-height)"
      >
        <i inline-flex i="dark:ep-moon ep-sunny" />
      </button>
    </el-menu-item>
  </el-menu>
  </div>
</template>

<style scoped>
.logo-container {
  display: inline-flex;
  align-items: center;
  padding-right: 87px;
}

.logo {
  width: 50px;
  height: 50px;
}
</style>

