const CheckUp = () => {
  const is_ipv4 = (text: string) => {
    const reg =
      /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    return reg.test(text);
  };
  const is_int = (text:string) =>{
    if(!/^\d+$/.test(text)) return false;
    return true;
  }
  return { is_ipv4,is_int };
};

const checkup = CheckUp();
export default checkup;
