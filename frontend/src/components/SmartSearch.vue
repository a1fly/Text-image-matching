<script>
import Header from "@/components/Header.vue";
import Asider from "@/components/Asider.vue";
import LostItemDisplay from "@/components/LostItemDisplay.vue";
import axios from "axios";
import {Loading} from "element-ui";

export default {
  components: {
    Header,
    Asider,
    LostItemDisplay
  },
  data() {
    return {
      UserInupt: "",
      isSidebarCollapsed: true,
      // Lostitem的数据
      items: []

    };
  },
  methods: {
    showIsSuccess(SuccessText) {
      this.$message({
        message: SuccessText,
        type: 'success',
        duration: 3000
      });
    },
    showError(ErrorText) {
      this.$message({
        message: ErrorText,
        type: 'error',
        duration: 3000
      });
    },
    updateStatus(value) {
      this.isSidebarCollapsed = value;
    },
    handleResize() {
      this.isSidebarCollapsed = window.innerWidth <= 768;
    },
    showQueriedItem()
    {
      // 展示查询到的失物条目


    },
    submitText() {
      if (this.UserInupt.trim().length === 0) {
        this.showError("不要只输入空格哦~");
        this.UserInupt = "";
        return;
      }
      // 启动加载动画
      const loadingInstance = Loading.service({
        lock: true,
        text: '狠狠计算中...',
        background: 'rgba(0, 0, 0, 0.7)',
      });
      axios
      .post('/api/UserText', {
        text: this.UserInupt
      })
      .then((response) => {
        let flag = response.data.issuccess;
        if (flag) {
          this.showIsSuccess("查找成功！！！");
          this.UserInupt = "";
          this.items = response.data.items;
        } else {
          this.showError("查找失败了，稍后再重试吧！");
        }
      })
      .catch((error) => {
        console.log(error);
        this.showError("请求失败，请检查网络连接或稍后重试！");
      })
      .finally(() => {
        // 关闭加载动画
        loadingInstance.close();
        this.showQueriedItem();
      });
    }
  },
  mounted() {
    // 初始化窗口大小监听
    window.addEventListener("resize", this.handleResize);
    this.handleResize(); // 初始化检测当前窗口大小
  },
  beforeDestroy() {
    // 移除窗口大小监听器
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<template>
  <div id="allbox">
    <el-container id="container">
      <!-- 头部 -->
      <el-header height="100px" class="header">
        <Header @toggle="updateStatus"></Header>
      </el-header>
      <el-container>
        <!-- 侧边栏 -->
        <el-aside
            class="aside"
            :style="{ width: isSidebarCollapsed ? '0px' : '250px' }"
        >
          <Asider></Asider>
        </el-aside>
        <!-- 主内容 -->
        <el-main class="main-content">

          <div class="Seach-content">
            <!-- 搜索的聊天框 -->
            <div class="SearchBox">

              <!--显示查找结果的地方 -->
              <div class="ResultShow">
                <LostItemDisplay :iteminfo="items"/>
              </div>

              <!--输入要搜索的内容的地方 -->
              <div class="SearchInput">
                <el-input
                    type="text"
                    placeholder="请输入内容"
                    v-model="UserInupt"
                    maxlength="20"
                    show-word-limit
                ></el-input>
                <el-button id="serachButton" type="primary" icon="el-icon-search" @click="submitText">
                  搜索
                </el-button>
                <el-button :plain="true" @click="showIsSuccess" style="display: none"></el-button>
              </div>
            </div>


          </div>


        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<style scoped>
#serachButton {
  color: #333333;
  margin-right: 10px;
  background-color: azure;
}

#serachButton:hover {
  background-color: #90e69d;
}

.SearchInput {
  margin-top: 20px;
  display: flex;
  gap: 7%;
  align-items: center;
}

.ResultShow {

  border: 2px solid #201c1c;
  background-color: #fff9f2;
  border-radius: 15px;
  height: 90%;
}

.Seach-content {
  width: 70%;
  height: 85%;
  display: flex;
  justify-content: center;
  margin-top: 1%;

}

.SearchBox {
  width: 70%;
  height: 100%;

  border-radius: 15px;
  overflow: hidden;
}


.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  background: linear-gradient(to right, #90e69d, #fad30c);
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 增加头部阴影 */
}


.el-container {
  display: flex;
  flex-direction: row;
  height: 100%;
}

.el-main {
  flex-grow: 1;
  min-width: 0;
  transition: padding-left 0.3s ease;
  display: flex;
  justify-content: center; /* 水平居中 */
  //align-items: center; /* 垂直居中 */
  background-color: #f5f7fa; /* 给主内容添加背景色 */
}

.center-content {
  text-align: center;
}


/* 布局基础样式 */
#allbox {
  width: 100%;
  height: 100%;
}

#container {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa; /* 整体背景色 */
}


/* 侧边栏样式 */
.el-aside {
  background-color: #ffffff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1); /* 增加侧边栏阴影 */
  overflow: hidden;
  transition: width 0.3s ease, transform 0.3s ease;
  position: fixed; /* 固定侧边栏，不挤压主内容 */
  height: 100%;
  z-index: 10;
  left: 0;
  border-right: 1px solid #ebeef5; /* 分隔线 */
}

.el-aside.collapsed {
  transform: translateX(-100%);
}


/* 响应式优化 */
@media (max-width: 768px) {
  .el-main {
    padding-left: 0;
  }
}

</style>