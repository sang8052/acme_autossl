/*
 * @Author: SudemQaQ
 * @Date: 2024-06-18 13:12:42
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-06-19 17:29:02
 * @Description: 
 */
/*
 * @Author: SudemQaQ
 * @Date: 2024-06-18 13:12:42
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-06-18 15:46:09
 * @Description: 
 */

import dayjs from "dayjs";

const hide_log = false;
// 美化打印实现方法
const prettyLog = () => {

  const isEmpty = (value: any) => value == null || value === undefined || value === '';
  const prettyPrint = (title: string, value: any, color: string) => {
    if (hide_log) return;
    const date =`[${   dayjs().format("YYYY-MM-DD HH:mm:ss SSS")  }]`;
    if(typeof(value) === 'string')  {
      console.log(
        `%c ${date} %c ${title} %c ${value} `,
        `background:${color};border:1px solid ${color}; padding: 1px; border-radius: 2px 0 0 2px; color: #fff;`,
        `border:1px solid ${color}; padding: 1px; border-radius: 0 2px 2px 0; color: ${color};`,
        'background:transparent'
      );
         
    }
    else{
      console.log(
        `%c ${date} %c ${title} `,
        `background:${color};border:1px solid ${color}; padding: 1px; border-radius: 2px 0 0 2px; color: #fff;`,
        `border:1px solid ${color}; padding: 1px; border-radius: 0 2px 2px 0; color: ${color};`,
        value
      );
    }
   

    
  };
  const info = (textOrTitle: string, content = '') => {
    const title = isEmpty(content) ? 'Info' : textOrTitle;
    const text = isEmpty(content) ? textOrTitle : content;
    prettyPrint(title, text, '#909399');
  };
  const error = (textOrTitle: string, content = '') => {
    const title = isEmpty(content) ? 'Error' : textOrTitle;
    const text = isEmpty(content) ? textOrTitle : content;
    prettyPrint(title, text, '#F56C6C');
  };
  const warning = (textOrTitle: string, content = '') => {
    const title = isEmpty(content) ? 'Warning' : textOrTitle;
    const text = isEmpty(content) ? textOrTitle : content;
    prettyPrint(title, text, '#E6A23C');
  };
  const success = (textOrTitle: string, content = '') => {
    const title = isEmpty(content) ? 'Success ' : textOrTitle;
    const text = isEmpty(content) ? textOrTitle : content;
    prettyPrint(title, text, '#67C23A');
  };
  
  const picture = (url: string, scale = 1) => {
    if (hide_log) return;
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      const c = document.createElement('canvas');
      const ctx = c.getContext('2d');
      if (ctx) {
        c.width = img.width;
        c.height = img.height;
        ctx.fillStyle = 'red';
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.drawImage(img, 0, 0);
        const dataUri = c.toDataURL('image/png');

        console.log(
          `%c sup?`,
          `font-size: 1px;
                    padding: ${Math.floor((img.height * scale) / 2)}px ${Math.floor((img.width * scale) / 2)}px;
                    background-image: url(${dataUri});
                    background-repeat: no-repeat;
                    background-size: ${img.width * scale}px ${img.height * scale}px;
                    color: transparent;
                    `
        );
      }
    };
    img.src = url;
  };

  return {
    info,
    error,
    warning,
    success,
    picture,
  };
};
const log = prettyLog();
export default log;