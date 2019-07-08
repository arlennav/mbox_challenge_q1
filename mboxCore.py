import os
import re
import asyncio
import aiofiles
from tqdm import tqdm

class MBOX:

    def __init__(self, mbox_dir,split_dir,filename,splitSignature):
        self.filename = filename
        self.mbox_dir = mbox_dir
        self.split_dir = split_dir
        self.splitSignature = splitSignature

    async def emailHeader(self,split_content):
        '''
        Separate Email Header
        '''
        emailHeader=[]
        for line in split_content:
            emailHeader.append(line)
            if 'Subject:' in line:
                return emailHeader
        
    async def reformat_Mbox(self,content):
        '''
        The new mbox file will have the emails in the same order, but with the lines of
        each individual message body printed in reverse order.
        The email headers and properly delimited email signatures remain unchanged.
        '''
        if content.replace("\n","").replace("\t","").strip()=='':
            #If content is blank do nothing
            return ''
        msgbodyList=[]
        emailHeaderList=[]
        split_content=content.split('\n')
        #Select Email Header
        emailHeaderList=await self.emailHeader(split_content)
        if self.splitSignature in content:
            # Select Message Body and Reverse Lines.
            msgbodyList=split_content[len(emailHeaderList):-2][::-1]
            # Add Signature
            msgbodyList.insert(len(msgbodyList),'-- ')
            msgbodyList.insert(len(msgbodyList),self.splitSignature) 
        else:
            msgbodyList=split_content[len(emailHeaderList)::][::-1]
        # Merge Email Header with Message Body 
        return '\n'.join(emailHeaderList+msgbodyList)
 
    async def splitFile(self):
        '''
        Spliting mbox file into separate individual email files
        '''
        async with aiofiles.open(f"{self.mbox_dir}{self.filename}", mode='r', encoding="ISO-8859-1") as f:
            try:            
                content = await f.read()
                lastpart=len(content.split(self.splitSignature))
                for i,part in enumerate(content.split(self.splitSignature)):
                    async with aiofiles.open(f"{self.split_dir}/{self.filename}_File_" + str(i+1), mode="w",encoding="utf8") as newfile:
                        if i!=lastpart-1:
                            await newfile.write(f"{part}{self.splitSignature}")
                        else:
                            await newfile.write(f"{part}")
            except Exception as exp:
                print(f"Error file {self.filename} {exp}")
                pass
      
    async def processFile(self,fname):
        '''
        Processing content of each splitted email files
        ''' 
        async with aiofiles.open(f"{self.split_dir}{fname}", mode='r', encoding="ISO-8859-1") as f:
            try:            
                content = await f.read()
                #Reformat mbox
                return await self.reformat_Mbox(content)
            except Exception as exp:
                print(f"Error file {fname} {exp}")
                pass        
       
    async def mbox(self):
        '''
        1.Spliting mbox file into separate individual email files
        '''
        print('Spliting mbox file')
        await self.splitFile()

        '''
        2.Generate new mbox file with all the changes
        '''    
        print('Processing files') 
        try:
            os.remove(f"{self.mbox_dir}{self.filename}_reversed")
        except OSError:
            pass
        async with aiofiles.open(f"{self.mbox_dir}{self.filename}_reversed", mode="a",encoding="ISO-8859-1") as out:
            for fname in tqdm(os.listdir(self.split_dir)):
                if fname.startswith(self.filename):
                    await out.write(await self.processFile(fname))
                out.flush()
        print(f"Input file: {self.mbox_dir}{self.filename}")
        print(f"Output file is generated: {self.mbox_dir}{self.filename}_reversed")
    