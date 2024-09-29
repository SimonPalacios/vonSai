
interface buttonProps {
  icon: string;
  id: string;
  href?: string;
  onClick?: () => void;
  title: string;
}

type cardProps = {
  item: RootObject;
  setToast: any;
  closeToast: any;
};

type toastProps = {
  title: string;
  text: string;
  footer?: any;
  close: any;
};