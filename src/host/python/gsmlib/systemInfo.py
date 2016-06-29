class systemInfo:
	#def callback(self,b,fn,state):
	#	ok,data = CCH.callback(self,b,fn,state)
	#	
	#	return 1,None
	@staticmethod
	def BitRow(c,pos):
		r = ['-']*8
		bit = ((c>>pos)&1)+0x31
		r[7-pos]=bit
		return ''.jion(r)

	@staticmethod
	def BitRowFill(c,mask):
		r = ['-']*8
		for i in range(8):
			if (mask>>i)&1:
				bit = ((c>>i)&1)
				r[7-i]=str(bit)
		return ''.join(r)

	def l2_Bits(self,data):
		print BCCH.BitRowFill(data[0], 0x70), (data[0] >> 4) & 7, 'TransactionID'
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
		if data[1]&0x3f in BCCH.rrmType:
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
		data = BCCH.l2_MccMncLac(data[1:])
		data = BCCH.CellSelectionParameters(data)
		data = BCCH.l2_RachControlParameters(data)
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
	@staticmethod
	def no_rrm(data):
		msg,f=BCCH.rrmType[data[0]&0x3f]
		print msg

	@staticmethod
	def l2_MccMncLac(data):
		ret = {}
		ret['mcc'] = [data[0] & 0x0f, (data[0] >> 4) & 0x0f, data[1] & 0x0f]
		ret['mnc'] = data[2] & 0x0f, (data[2] >> 4) & 0x0f, (data[1] >> 4) & 0x0f
		ret['lac'] = (data[3] << 8) | data[4]
		print ret
		return data[5:]
	@staticmethod
	def CellSelectionParameters(data):
		print BCCH.BitRowFill(data[0],0xe0), 'Cell Reselect Hyst.',(data[0]>>5)*2,'dB'
		print BCCH.BitRowFill(data[0],0x1f), 'Max Tx power level:',data[0]&0x1f
		if data[1] >> 7:
			print '1------- Additional cells in SysInfo 16,17'
		else:
			print '0------- No additional cells in SysInfo 7-8'
		if ((data[1] >> 6) & 1):
			print '-1------ New establishm cause: supported'
		else:
			print '0------ New establishm cause: not supported'
		print BCCH.BitRowFill(data[1],0x3f),'RXLEV Access Min permitted = -110 + %ddB'%(data[1]&0x3f)
		return data[2:]
	@staticmethod
	def l2_RachControlParameters(data):
		print 'RachControlParameters',data
		return data

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
			, 0x15:('00010101 RR Measurement Report C [FIXME]',BCCH.no_rrm)
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