from CCH import CCH
from config import *
from GSM import *
import numpy as np

class BCCH(CCH):
	__name__="bcch"

	__type__ = ['1','2','3','4or8','9or2ter','2teror2bit','3','4or7']

	def __init__(self):
		CCH.__init__(self)

	def attach(self,C):
		for i in range(2,6):
			f = C.frame[i]
			x = f[0]
			x.attach(self)
	
	def deattach(self,C):
		for i in range(2,6):
			f = C.frame[i]
			x = f[0]
			x.deattach()

	def callback(self,b,fn,state):
		ok,data = CCH.callback(self,b,fn,state)
		if ok=='newdata':
			self.l2_Bits(data[1:])
		return 1,None

	def BitRow(self,c,pos):
		"""
		static char *
		BitRow(unsigned char c, int pos)
		{
			unsigned char bit = 0;
			static char buf[9];

			if ((c >> pos) & 1)
				bit = 1;

			if (pos == 0)
				snprintf(buf, sizeof buf, "-------%d", bit);
			else if (pos == 1)
				snprintf(buf, sizeof buf, "------%d-", bit);
			else if (pos == 2)
				snprintf(buf, sizeof buf, "-----%d--", bit);
			else if (pos == 3)
				snprintf(buf, sizeof buf, "----%d---", bit);
			else if (pos == 4)
				snprintf(buf, sizeof buf, "---%d----", bit);
			else if (pos == 5)
				snprintf(buf, sizeof buf, "--%d-----", bit);
			else if (pos == 6)
				snprintf(buf, sizeof buf, "-%d------", bit);
			else if (pos == 7)
				snprintf(buf, sizeof buf, "%d-------", bit);

			return buf;
		}
		"""
		r = ['-']*8
		bit = ((c>>pos)&1)+0x31
		r[7-pos]=bit
		return ''.jion(r)
	def BitRowFill(self,c,mask):
		"""
		static char *
		BitRowFill(unsigned char c, unsigned char mask)
		{
			static char buf[9];
			
			memset(buf, '-', sizeof buf);
			buf[sizeof buf - 1] = '\0';
			int i = 0;
			while (i < 8)
			{
				if ((mask >> i) & 1)
				{
					if ((c >> i) & 1)
						buf[7 - i] = '1';
					else
						buf[7 - i] = '0';
				}
				i++;
			}

			return buf;
		}
		"""
		r = ['-']*8
		for i in range(8):
			if (mask>>i)&1:
				bit = ((c>>i)&1)
				r[7-i]=str(bit)
		return ''.join(r)

	def l2_Bits(self,data):
		"""
		static void
		l2_Bbis()
		{
			if (data >= end)
				RETTRUNK();

			switch (data[0] >> 7)
			{
			case 1:
				OUTF("1------- Direction: To originating site\n");
				break;
			default:
				OUTF("0------- Direction: From originating site\n");
			}

			OUTF("%s %d TransactionID\n", BitRowFill(data[0], 0x70), (data[0] >> 4) & 7);

			switch (data[0] & 0x0f)
			{
			case 0:
				OUTF("----0000 Group Call Control [FIXME]\n");
				break;
			case 1:
				OUTF("----0001 Broadcast call control [FIXME]\n");
				data++;
				l2_bcc();
				/* TS GSM 04.69 */
				break;
			case 2:
				OUTF("----0010 PDSS1 [FIXME]\n");
				break;
			case 3:
				OUTF("----0011 Call control. call related SS messages\n");
				data++;
				l2_cc();
				/* TS 24.008 */
				break;
			case 4:
				OUTF("----01-- PDSS2 [FIXME]\n");
				break;
			case 5:
				OUTF("----0101 Mobile Management Message (non GPRS)\n");
				data++;
				/* TS 24.008 */
				l2_mmm();
				break;
			case 6:
				OUTF("----0110 Radio Resouce Management\n");
				data++;
				l2_rrm();
				break;
			case 7:
				OUTF("----0111 RFU [FIXME]\n");
				break;
			case 8:
				OUTF("----1000 GPRS Mobile Management\n");
				/* in GMMattachAccept */
				/* in GMMidentityRequest */
				OUTF("FIXME: possible IMEI in here\n");
				break;
			case 9:
				OUTF("----1001 SMS messages\n");
				data++;
				l2_sms();
				/* TS 04.11 */
				break;
			case 0x0a:
				OUTF("----1011 GRPS session management messages [FIXME]\n");
				break;
			case 0x0b:
				OUTF("----1011 Non-call related SS messages [FIXME]\n");
				/* GSM 04.80 */
				break;
			case 0x0c:
				OUTF("----1100 Location services [FIXME]\n");
				break;
			case 0x0d:
				OUTF("----1101 RFU [FIXME]\n");
				break;
			case 0x0e:
				OUTF("----1110 Extension of the PD to one octet length [FIXME]\n");
				break;
			case 0x0f:
				OUTF("----1111 Tests procedures describe in TS GSM 11.10 [FIXME]\n");
				break;
			default:
				OUTF("%s 0x%02x UNKNOWN\n", BitRowFill(data[0], 0x0f), data[0] & 0x0f);
			}

		}
		"""
		print self.BitRowFill(data[0], 0x70), (data[0] >> 4) & 7, 'TransactionID'
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		f(data)
		
		
	@staticmethod
	def no_decode(data):
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		print msg
	@staticmethod
	def l2_bcc(data):
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		print msg
	@staticmethod
	def l2_cc(data):
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		print msg
	@staticmethod
	def l2_mmm(data):
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		print msg
	@staticmethod
	def l2_rrm(data):
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		print msg
		(msg,f) = BCCH.rrmType[data[1]&0x3f]
		f(data[1:])

	@staticmethod
	def l2_sms(data):
		(i,msg,f) = BCCH.msgType[data[0]&0xf]
		print msg

	@staticmethod
	def l2_RRsystemInfo13C(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_BcchAllocation(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_ChannelRelease(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRclassmarkChange(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRsystemInfo1(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRsystemInfo2(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRsystemInfo3C(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRsystemInfo4C(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_NeighbourCellDescription(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRsystemInfo6(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRpagingrequest1(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRpagingrequest2(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRpagingrequest3(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRpagingresponse(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRassignComplete(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRassignCommand(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRciphModCompl(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRciphModCmd(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
	@staticmethod
	def l2_RRimmediateAssignment(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg
BCCH.msgType = [
			  (0x0,'----0000 Group Call Control'                     ,BCCH.no_decode)
			, (0x1,'----0001 Broadcast call control'                 ,BCCH.l2_bcc   )
			, (0x2,'----0010 PDSS1'                                  ,BCCH.no_decode)
			, (0x3,'----0011 Call control. call related SS messages' ,BCCH.l2_cc    )
			, (0x4,'----01-- PDSS2'                                  ,BCCH.no_decode)
			, (0x5,'----0101 Mobile Management Message (non GPRS)'   ,BCCH.l2_mmm   )
			, (0x6,'----0110 Radio Resouce Management'               ,BCCH.l2_rrm   )
			, (0x7,'----0111 RFU'                                    ,BCCH.no_decode)
			, (0x8,'----1000 GPRS Mobile Management'                 ,BCCH.no_decode)
			, (0x9,'----1001 SMS messages'                           ,BCCH.l2_sms   )
			, (0xa,'----1010 GRPS session management messages'       ,BCCH.no_decode)
			, (0xb,'----1011 Non-call related SS messages'           ,BCCH.no_decode)
			, (0xd,'----1101 RFU'                                    ,BCCH.no_decode)
			, (0xe,'----1110 Extension of the PD to one octet length',BCCH.no_decode)
			, (0xf,'----1111 Tests proc describe in TS GSM 11.10'    ,BCCH.no_decode)
		]


BCCH.rrmType = {
			  0x00:('00000000 System Information Type 13',BCCH.l2_RRsystemInfo13C)
			, 0x06:('00000110 System Information Type 5ter',BCCH.l2_BcchAllocation)
			, 0x0d:('00001101 Channel Release',BCCH.l2_ChannelRelease)
			, 0x15:('00010101 RR Measurement Report C [FIXME]',)
			, 0x16:('00010110 RRclassmarkChange',BCCH.l2_RRclassmarkChange)
			, 0x19:('00011001 RRsystemInfo1',BCCH.l2_RRsystemInfo1)
			, 0x1a:('00011010 RRsystemInfo2',BCCH.l2_RRsystemInfo2)
			, 0x1b:('00011011 RRsystemInfo3C',BCCH.l2_RRsystemInfo3C)
			, 0x1c:('00011100 RRsystemInfo4-C',BCCH.l2_RRsystemInfo4C)
			, 0x1d:('00011101 Neighbour Cells Description',BCCH.l2_NeighbourCellDescription)
			, 0x1e:('00011110 System Information Type 6',BCCH.l2_RRsystemInfo6)
			, 0x21:('00100001 Paging Request Type 1',BCCH.l2_RRpagingrequest1)
			, 0x22:('00100010 Paging Request Type 2',BCCH.l2_RRpagingrequest2)
			, 0x24:('00100100 Paging Request Type 3',BCCH.l2_RRpagingrequest3)
			, 0x27:('0-100111 RRpagingResponse',BCCH.l2_RRpagingresponse)
			, 0x29:('0-101001 RR Assign Complete',BCCH.l2_RRassignComplete)
			, 0x2e:('00101110 RR Assign Command',BCCH.l2_RRassignCommand)
			, 0x32:('00110010 RR Cipher Mode Complete',BCCH.l2_RRciphModCompl)
			, 0x35:('00110101 RR Cipher Mode Command',BCCH.l2_RRciphModCmd)
			, 0x3f:('0-111111 RRimmediateAssignment',BCCH.l2_RRimmediateAssignment)
}