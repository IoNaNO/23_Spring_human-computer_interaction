<template>
  <el-config-provider namespace="ep">
    <BaseHeader />
    <div style="display: flex">
      <BaseSide />
      <div>
        <img alt="search logo" class="search-logo" src="./assets/logo.png" />
        <router-view/>
      </div>
    </div>
  </el-config-provider>
</template>

<style>
#app {
  text-align: center;
  color: var(--ep-text-color-primary);
}

.search-logo {
  justify-content: center;
  width: 1000px;
  display: block;
}
</style>

<script lang="ts">
import { defineComponent } from "vue";
// import router from "./router"

export default defineComponent({
})
</script>