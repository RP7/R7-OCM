#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/types.h> 
typedef struct IpInfo {
	int len;
	struct sockaddr_in servaddr;
	int wlast;
} IpInfo_t;
	
class udpClient {
	private:
		int sockfd;
		struct sockaddr_in servaddr;
		int addr_len; 
      
	public:
		IpInfo_t peer;
		udpClient( const char *ip, unsigned short port )
		{
		    	addr_len =sizeof(struct sockaddr_in);
		    	sockfd = socket(PF_INET, SOCK_DGRAM, 0);
    			bzero(&servaddr, sizeof(servaddr));
    			servaddr.sin_family = AF_INET;
    			servaddr.sin_port = htons(port);
    			servaddr.sin_addr.s_addr = inet_addr(ip);
  		};

		~udpClient( ) { close(sockfd); };

		int send( char *sendline, int len ) 
		{
			return sendto( sockfd
				, sendline
				, len
				, 0
				, (struct sockaddr *)&servaddr
				, addr_len
				);
		};
		int sendtoPeer( char *sendline, int len )
		{
			return sendto( sockfd
				, sendline
				, len
				, 0
				, (struct sockaddr *)&(peer.servaddr)
				, peer.len
				);
		}
		int recv( char *buf, int len )
		{
			return recvfrom( sockfd
				, buf
				, len
				, 0
				, 0
				, 0 );
		};
};

class udpServer
{
	private:
		int sockfd;
		struct sockaddr_in servaddr;
		int addr_len; 
	public:
      	IpInfo_t peer;
		udpServer( unsigned short port = 11043 )
		{
		    	addr_len =sizeof(struct sockaddr_in);
		    	sockfd = socket(PF_INET, SOCK_DGRAM, 0);
		    	int flag = 1;
		    	setsockopt( sockfd, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(int));
    
    			bzero(&servaddr, sizeof(servaddr));
    			servaddr.sin_family = AF_INET;
    			servaddr.sin_port = htons(port);
    			servaddr.sin_addr.s_addr = htons(INADDR_ANY);
    			bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
  		};

		~udpServer( ) { close(sockfd); };

		int send( char *sendline, int len ) 
		{
			if( peer.len==0 )
			{
				printf("unknow peer\n");
				return -1;
			}
			else
			{
				return sendto( sockfd
					, sendline
					, len
					, 0
					, (struct sockaddr *)&(peer.servaddr)
					, peer.len
					);
			}
		};
		int recv( char *buf, int len )
		{
			return recvfrom( sockfd
				, buf
				, len
				, 0
				, (struct sockaddr *)&(peer.servaddr)
				, (socklen_t*)&(peer.len) );
		};
		int reportPeerIP()
		{
			printf("receive from %s\n" , inet_ntoa( peer.servaddr.sin_addr ));
			return 0;
		};
		IpInfo_t *peerIpInfo()
		{
			return &peer;
		}
	
};

