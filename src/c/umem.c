#include <linux/proc_fs.h>
static struct proc_dir_entry *umem_root = NULL;  
static struct proc_dir_entry *init_entry = NULL;
static struct proc_dir_entry *deinit_entry = NULL;

#define UMEM_ROOT_DIR "umem"  
#define UMEM_INIT     "init"
#define UMEM_DEINIT   "deinit"

static char last_init_result[256];
static char last_deinit_result[256];

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
	init_entry = create_proc_entry(UMEM_INIT, 0666, umem_root); 
	if ( NULL == init_entry ) 
	{ 
		printk(KERN_ALERT"Create entry %s under /proc/%s error!\n", 
						UMEM_INIT,UMEM_ROOT_DIR); 
		goto err_out_init; 
	}
	
	init_entry->write_proc= umem_init_writeproc;
	init_entry->read_proc =umem_init_readproc;
	printk(KERN_INFO"Create /proc/%s/%s\n", 
		   UMEM_ROOT_DIR,UMEM_INIT);  
	
	// Create deinit under UMEM_ROOT_DIR 
	deinit_entry = create_proc_entry(UMEM_DEINIT, 0666, umem_root); 
	if ( NULL == deinit_entry ) 
	{ 
		printk(KERN_ALERT"Create entry %s under /proc/%s error!\n", 
						UMEM_DEINIT,UMEM_ROOT_DIR); 
		goto err_out_deinit; 
	}
	
	deinit_entry->write_proc= umem_deinit_writeproc;
	deinit_entry->read_proc = umem_deinit_readproc;
	printk(KERN_INFO"Create /proc/%s/%s\n", 
		   UMEM_ROOT_DIR,UMEM_DEINIT);  
	
	return 0; 
	
err_out_deinit: 
	deinit_entry->read_proc =NULL; 
	deinit_entry->write_proc= NULL;
	remove_proc_entry(UMEM_INIT,init_entry); 
err_out_init: 
	init_entry->read_proc =NULL; 
	init_entry->write_proc= NULL;
	remove_proc_entry(UMEM_ROOT_DIR,umem_root); 
	return -1; 
}

static int umem_init_writeproc(struct file *file,const char *buffer,
			      unsigned long count,void *data)
{
	char Name[128];
	char Len[128];
	int length;
	int i;
	sscanf(buffer,"%s %s", Name, Len);
	i = strlen(Len);
	if(Len[i-1]=='M')
	{
		Len[i-1]='\0';
		length = atoi(Len)*0x100000;
	}
	else if(Len[i-1]=='K')
	{
		Len[i-1]='\0';
		length = atoi(Len)*0x400;
	}
	else
		length = atoi(Len);	
	printk("umem: proc-->init = Name:%s, Size:%s[0x%x]\n", Name,Len,length);
	if((length%0x1000)!=0)
		sprintf(last_init_result,"{'ret':'length not align to pagesize 4K\n'}");
	if(length==0)
		sprintf(last_init_result,"{'ret':'nothing to do'}");
	return count;
}

static int umem_init_readproc(char *page, char **start, off_t off,
						int count,int *eof, void *data)
{
	count = sprintf(page,"%s", last_init_result);
	return count;
}

static int umem_deinit_writeproc(struct file *file,const char *buffer,
						unsigned long count,void *data)
{
	char Name[128];
	sscanf(buffer,"%s", Name);
	printk("umem: proc-->deinit = %s\n", Name);
	return count;
}

static int umem_deinit_readproc(char *page, char **start, off_t off,
						int count,int *eof, void *data)
{
	count = sprintf(page,"%s", last_deinit_result);
	return count;
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
