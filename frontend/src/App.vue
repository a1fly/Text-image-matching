<template>
  <div id="app">
    <router-view></router-view> <!-- 这里将显示匹配的组件 -->
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
</style>
