<template>
  <div id="LoginContainer">
    <div class="left-side">
      <!-- 打字机效果 -->
      <div class="typewriter" ref="typewriter"></div>
    </div>
    <div class="right-side">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="60px" class="demo-ruleForm">
        <h1 class="login-header">注册</h1>
        <el-form-item label="账号" prop="acc" class="loginItem">
          <el-input class="Regtextinput" v-model="ruleForm.acc" autocomplete="off" placeholder="请输入账号"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="pass" class="loginItem">
          <el-input class="Regtextinput" type="password" show-password v-model="ruleForm.pass" autocomplete="off"
                    placeholder="请输入密码"></el-input>
        </el-form-item>

        <el-form-item label="确认" prop="confirmPass" class="loginItem">
          <el-input class="Regtextinput" type="password" show-password v-model="ruleForm.confirmPass" autocomplete="off"
                    placeholder="请输入确认密码"></el-input>
        </el-form-item>


        <el-form-item label="联系" prop="contact" class="loginItem">
          <el-select v-model="Contact" placeholder="请选择联系方式" class="Regtextinput">
            <el-option
                v-for="item in options"
                :key="item.Contact"
                :label="item.label"
                :value="item.label">
            </el-option>
          </el-select>
          <p></p>

          <el-input class="Regtextinput" v-model="Contact_Num" :placeholder="`请输入${Contact}号`">></el-input>
        </el-form-item>


        <el-form-item class="loginItem">
          <el-button class="regbutton" style="background-color: #f1ffc4" @click="submitForm('ruleForm')">注册
          </el-button>
          <el-button type="text" @click="goToLogin" style="margin-left: 43%; ">返回登录</el-button>
        </el-form-item>


      </el-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {

  data() {
    return {
      Contact_Num: '',
      options: [{
        Contact: '选项1',
        label: '微信'
      }, {
        Contact: '选项2',
        label: 'QQ'
      }, {
        Contact: '选项3',
        label: '钉钉'
      }],
      Contact: '',
      ruleForm: {
        acc: '',
        pass: '',
        confirmPass: ''
      },
      rules: {
        acc: [
          {required: true, message: '请输入账号', trigger: 'blur'}
        ],
        pass: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 6, message: '密码长度至少为6位', trigger: 'blur'}
        ],
        confirmPass: [
          {required: true, message: '请确认密码', trigger: 'blur'},
          {validator: this.validateConfirmPass, trigger: 'blur'}
        ]
      }
    };
  },
  methods: {

    goToLogin() {
      this.$router.push('/login');
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log("联系方式类型：",this.Contact)
          console.log("用户名：",this.ruleForm.acc)
          console.log("密码：",this.ruleForm.pass)
          console.log("联系号码：",this.Contact_Num)
          // 准备要发送的表单数据
          const formData = {
            contactType: this.Contact,    // 联系方式类型
            username: this.ruleForm.acc,  // 用户名
            password: this.ruleForm.pass, // 密码
            contactNumber: this.Contact_Num // 联系号码
          };

          // 发送 POST 请求到 /api/reg
          axios.post('/api/reg', formData)
              .then(response => {
                // 请求成功后的回调
                if (response.data.success)
                {
                  console.log('注册成功：', response.data);
                  alert('注册成功！');
                  this.$router.push('/login');
                }else
                {
                  alert('注册失败');
                }

              })
              .catch(error => {
                // 请求失败后的回调
                console.log('注册失败：', error);
                alert('注册失败，请重试！');
              });

        } else {
          console.log('表单验证失败！');
          return false;
        }
      });
    },
    validateConfirmPass(rule, value, callback) {
      if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    },

    typewriterEffect(text, element, index = 0) {
      if (index < text.length) {
        const currentChar = text.charAt(index);
        if (currentChar === ',') {
          element.textContent += '\n';
        } else {
          element.textContent += currentChar;
        }
        setTimeout(() => this.typewriterEffect(text, element, index + 1), 100);
      }
    }
  },
  mounted() {
    const text = "欢迎注册！！！";
    const typewriterElement = this.$refs.typewriter;
    this.typewriterEffect(text, typewriterElement);
  }
};
</script>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.regbutton {
  width: 100%;
  margin-top: 20px;
}

.regbutton:hover {
  background-color: #ee0979;
  border-color: #ee0979;
}


#LoginContainer {
  display: flex;
  height: 100%;
  background: linear-gradient(135deg, #1aa4ff, #ee0979);
  color: white;
  justify-content: center; /* 中央对齐整个容器 */
}

.left-side {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-left: 50px; /* 为左侧增加一点间距 */
}

.typewriter {
  font-size: 36px; /* 适当缩小字体大小 */
  color: white;
  font-weight: bold;
  white-space: pre-wrap;
  text-align: center;
}

.right-side {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.demo-ruleForm {
  background: rgba(255, 255, 255, 0.9);
  padding: 30px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 450px; /* 设置表单宽度 */
  min-height: 500px; /* 确保表单足够高 */
}

.login-header {
  font-size: 28px;
  color: #333;
  text-align: center;
  margin-bottom: 30px; /* 为标题和表单之间增加间距 */
}

.loginItem {
  margin-top: 20px;
  width: 100%; /* 保证每个表单项占满整个表单宽度 */
}

.Regtextinput {
  width: 100%;
}

.el-form-item__label {
  color: #333;
  font-weight: bold;
}

.el-input__inner, .el-select__inner {
  background: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: #333;
  padding-left: 15px; /* 为输入框和选择框加一点内边距 */
  height: 40px; /* 设置高度 */
}


</style>
