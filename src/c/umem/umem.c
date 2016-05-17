#include <linux/proc_fs.h>
#include <linux/module.h>

static struct proc_dir_entry *umem_root = NULL;  
static struct proc_dir_entry *init_entry = NULL;
static struct proc_dir_entry *deinit_entry = NULL;

#define UMEM_ROOT_DIR "umem"  
#define UMEM_INIT     "init"
#define UMEM_DEINIT   "deinit"

static char last_init_result[256];
static char last_deinit_result[256];

static size_t umem_init_writeproc(struct file *file,const char *buffer,
						size_t count, loff_t *data)
{
	char Name[128];
	char Len[128];
	char *after;
	int length;
	int i;
	sscanf(buffer,"%s %s", Name, Len);
	i = strlen(Len);
	length = simple_strtol(Len,&after,10);
	if(*after=='M')
	{
		length *= 0x100000;
	}
	else if(*after=='K')
	{
		length *= 0x400;
	}
	printk("umem: proc-->init = Name:%s, Size:%s[0x%x]\n", Name,Len,length);
	if((length%0x1000)!=0)
		sprintf(last_init_result,"{'ret':'length not align to pagesize 4K\n'}");
	if(length==0)
		sprintf(last_init_result,"{'ret':'nothing to do'}");
	return count;
}

static size_t umem_init_readproc(struct file * file, char __user *page, 
	size_t count, loff_t *data)
{
	count = sprintf(page,"%s", last_init_result);
	return count;
}

static size_t umem_deinit_writeproc(struct file *file,const char *buffer,
						size_t count, loff_t *data)
{
	char Name[128];
	sscanf(buffer,"%s", Name);
	printk("umem: proc-->deinit = %s\n", Name);
	return count;
}

static size_t umem_deinit_readproc(struct file * file, char __user *page, 
	size_t count, loff_t *data)
{
	count = sprintf(page,"%s", last_deinit_result);
	return count;
}

static struct file_operations init_fops = {
	.read  = umem_init_readproc,
	.write = umem_init_writeproc
};

static struct file_operations deinit_fops = {
	.read  = umem_deinit_readproc,
	.write = umem_deinit_writeproc
};

static int init_umem(void)
{
	umem_root = proc_mkdir(UMEM_ROOT_DIR, NULL); 
	if ( NULL == umem_root ) 
	{ 
		printk(KERN_ALERT"Create dir /proc/%s error!\n", UMEM_ROOT_DIR); 
		return -1; 
	} 
	printk( KERN_INFO"Create dir /proc/%s\n", UMEM_ROOT_DIR ); 
	
	// Create init under UMEM_ROOT_DIR 
	init_entry = proc_create(UMEM_INIT, 0666, umem_root, &init_fops); 
	if ( NULL == init_entry ) 
	{ 
		printk(KERN_ALERT"Create entry %s under /proc/%s error!\n", 
						UMEM_INIT,UMEM_ROOT_DIR); 
		goto err_out_init; 
	}
	printk(KERN_INFO"Create /proc/%s/%s\n", 
		   UMEM_ROOT_DIR,UMEM_INIT);  
	
	// Create deinit under UMEM_ROOT_DIR 
	deinit_entry = proc_create(UMEM_DEINIT, 0666, umem_root, &deinit_fops); 
	if ( NULL == deinit_entry ) 
	{ 
		printk(KERN_ALERT"Create entry %s under /proc/%s error!\n", 
						UMEM_DEINIT,UMEM_ROOT_DIR); 
		goto err_out_deinit; 
	}
	
	printk(KERN_INFO"Create /proc/%s/%s\n", 
		   UMEM_ROOT_DIR,UMEM_DEINIT);  
	
	return 0; 
	
err_out_deinit: 
	remove_proc_entry(UMEM_INIT,init_entry); 
err_out_init: 
	remove_proc_entry(UMEM_ROOT_DIR,umem_root); 
	return -1; 
}

static void deinit_umem(void)
{
	remove_proc_entry(UMEM_INIT,init_entry);
	remove_proc_entry(UMEM_INIT,deinit_entry);
	remove_proc_entry(UMEM_ROOT_DIR,umem_root);
}

static int __init umem_init(void) 
{
  init_umem();
  return 0;
}

static void __exit umem_exit(void)
{
	deinit_umem();
}

module_init(umem_init);
module_exit(umem_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("a4a881d4");
MODULE_VERSION("1.0");
