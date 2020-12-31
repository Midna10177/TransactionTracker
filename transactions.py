import os,pickle,time
def moneyfmt(x): return "${:,.2f}".format(x)+''
class Transaction:
	def __init__(self,amt,nts):
		self.amount=amt
		self.notes=nts
		self.ts=time.time()
		
	def __repr__(self):
		return(moneyfmt(self.amount)+': '+str(self.notes)+', '+time.ctime(self.ts))
		
class TransactionHistory:
	def __init__(self):
		self.transactions=list()
		
	def pop(self): return self.transactions.pop()
	
	def delete(self,index):
		index=int(index)
		del self.transactions[index]
		
	def add(self,amount,notes):
		if type(amount) not in [int,float]:
			raise ValueError('Amount must be number')
		if type(amount)==float:
			amount=round(amount,2)
		a,d=amount,notes
		self.transactions.append(Transaction(a,d))
		
	def balance(self):
		return moneyfmt(sum([x.amount for x in self.transactions]))
	def edit(self,index,amount=None,notes=None):
		if amount == None:
			amount=self.transactions[index].amount
		if notes == None:
			notes=self.transactions[index].notes
		self.transactions[index].amount = amount
		self.transactions[index].notes=notes
	def __repr__(self):
		o='[\n'
		d='\n'.join([' ['+str(c)+'] '+str(x) for c,x in enumerate(self.transactions)])
		o+=d+'\n] balance:'+str(self.balance())
		return o


if __name__=='__main__':
	target='transaction_history'
	root='/storage/emulated/0/'
	file=os.path.join(root,target)
	
	hist=TransactionHistory()
	if os.path.isfile(file):
		hist=pickle.load(open(file,"rb"))
	def save():
		pickle.dump(hist,open(file,'wb'))
		print('saved to',file)
	while(True):
		print('-'*60)
		print(hist)
		i=input('\n\ncontrol codes:\n c to create new transaction, or\n s to save, or\n d to delete a transaction\n u to remove newest transaction\n e to edit a transaction\n delfile to delete save file: ')
		i=i.lower().strip()
		if i=='c':
			a=float(input('\nenter amount: '))
			if a-int(a) == 0: a=int(a)
			d=input('enter any notes youd like: ')
			hist.add(a,d)
		elif i=='s':
			save()
		elif i=='d':
			n=input('\nenter index to delete: ')
			hist.delete(n)
		elif i=='u':
			hist.pop()
		elif i=='delfile':
			try:
				os.remove(file)
			except:
				print('error thrown for file deletion')
		elif i == 'e':
			ind=input('enter the index to edit: ')
			ind=int(ind.strip())
			print('selected, '+str(hist.transactions[ind]))
			a=input('enter amount (press enter to keep same): ')
			n=input('enter notes (press enter to keep same): ')
			if a.lower().strip() == '': a=None
			if n.lower().strip() == '': n=None
			hist.edit(ind,a,n)