<template>
  <div id="LoginContainer">
    <div class="left-side">
      <!-- 打字机效果 -->
      <div class="typewriter" ref="typewriter"></div>
    </div>
    <div class="right-side">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="60px" class="demo-ruleForm">
        <h1 class="login-header">登录</h1>
        <el-form-item label="账号" prop="acc" class="loginItem" :required="false">
          <el-input  v-model="ruleForm.acc" autocomplete="off" placeholder="请输入账号"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="pass" class="loginItem" :required="false">
          <el-input type="password" show-password v-model="ruleForm.pass" autocomplete="off" placeholder="请输入密码"></el-input>
        </el-form-item>

        <el-form-item class="loginItem">
          <el-button id="sub_button" type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button  @click="GotoReg()">注册</el-button>
          <el-button type="text" @click="forgetPassword" class="forget-password" style="margin-left: 60px; ">忘记密码</el-button>
        </el-form-item>

      </el-form>
    </div>
  </div>
</template>

<script>
import { SHA256 } from 'crypto-js';
import axios from 'axios';

export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else if (value.length < 6) {
        callback(new Error('密码长度至少为6位'));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        acc: '',
        pass: ''
      },
      rules: {
        acc: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        pass: [
          { validator: validatePass, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const hashedPassword = SHA256(this.ruleForm.pass).toString();
          // 发送请求到服务器
          axios.post('/api/login', {
            acc: this.ruleForm.acc,
            pass: hashedPassword
          }).then(response => {
            console.log(response);
            alert('登录成功！');
            // 处理登录成功的逻辑
          }).catch(error => {
            console.error('登录失败:', error);
            alert('登录失败，请检查账号和密码');
          });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },

    GotoReg(){
      this.$router.push('/reg');
    },

    forgetPassword() {
      // 处理忘记密码的逻辑
      // 例如，跳转到忘记密码页面
      this.$router.push('/forget_password');
      // 或者显示一个模态框
      // this.$alert('请提供您的邮箱地址以重置密码', '忘记密码', {
      //   confirmButtonText: '确定',
      //   callback: action => {
      //     this.$message({
      //       type: 'info',
      //       message: `action: ${action}`
      //     });
      //   }
      // });
    },
    typewriterEffect(text, element, index = 0) {
      if (index < text.length) {
        const currentChar = text.charAt(index);
        if (currentChar === ',') {
          element.textContent += '\n'; // 遇到逗号时换行
        } else {
          element.textContent += currentChar;
        }
        setTimeout(() => this.typewriterEffect(text, element, index + 1), 100);
      }
    }
  },
  mounted() {
    const text = "自然语言,or,物品图片,find,丢失物品";
    const typewriterElement = this.$refs.typewriter;
    this.typewriterEffect(text, typewriterElement);
  }
}
</script>

<style  scoped>

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#LoginContainer {
  display: flex;
  height: 100%;
  background: linear-gradient(135deg, #1aa4ff, #ee0979);
  color: white;
}

.left-side {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.typewriter {

  font-size: 42px;
  color: white;
  font-weight: bold;
  white-space: pre-wrap; /* 使换行生效 */
  text-align: center; /* 水平居中 */
  margin-left: 50px;
}





.el-form-item__label {
  color: #333;
}

.el-input__inner {
  background: transparent;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: #333;
}




#sub_button {
  background: #ff6a00;
  border-color: #ff6a00;
}

#sub_button:hover {
  background: #ee0979;
  border-color: #ee0979;
}


.el-button--text.forget-password {
  color: #ff6a00;
  font-size: 14px;
}

.el-button--text.forget-password:hover {
  color: #ee0979;
}

.loginItem{
  margin-top: 30px;

}
.login-header {
  font-size: 24px;
  color: #333;
  text-align: center;
}
.right-side {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;

}

.demo-ruleForm {
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 400px;
  height: 300px;
}
</style>