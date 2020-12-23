''' JSON session manager '''
import os
import json
from hashlib import blake2s

import aiofiles
from PIL import Image
from pySmartDL import SmartDL

from pyrogram import Client, types, crypto

from assistant import Config

AES_PASS = blake2s(Config.AES_DB_PASS.encode()).digest()
VI_KEY = blake2s(Config.DB_VI_KEY.encode()).digest()
LOG_ID = Config.DB_CHANNEL

SES_DIR = './.json-session'
SES_FILZ = {
    'test': 'test-session.json'
}


class JsonSeVe:
    ''' ╮(╯▽╰)╭ '''

    def __init__(self, session: str, save_id: int = 0):
        ''' Initialization of Json Save
            param: session :-> name of session like warn, etc that exists in SES_FILZ
            param: save_id :-> message id of a media that is to be edited.
        '''
        self.jthumb = os.path.abspath('./.thumbs/jsumb.jpeg')
        self.thumb_uri = 'https://telegra.ph/file/da08e43d19d5023a248be.jpg'
        self.tg_save = save_id
        self.dir = SES_DIR
        self.session = session
        self.file = SES_FILZ.get(self.session)
        self.ses_path = os.path.abspath(str(self.dir) + '/' + (self.file))
        self.ses_path_enc = self.ses_path + '.enc'
        if not os.path.lexists(self.dir):
            os.makedirs(self.dir)
        if not os.path.lexists('./.thumbs'):
            os.makedirs('./.thumbs')
        if not os.path.isfile(self.jthumb):
            dl_thumb = SmartDL(self.thumb_uri, self.jthumb, progress_bar=True)
            dl_thumb.start(blocking=True)
            img = Image.open(self.jthumb)
            img.resize((320, 320))
            img.save(self.jthumb)

    @staticmethod
    def _add_buffer(data: bytes):
        ''' add white spaces as multiples of 16 is required for encryption '''
        lez = len(data)
        if lez % 16 != 0:
            data += b' ' * (16 - lez % 16)
        return data

    async def encrypt_data(self):
        ''' makes a copy of encrypted data '''
        async with aiofiles.open(self.ses_path, 'rb') as enc:
            data = await enc.readlines()
        enc_data = []
        for line in data:
            line = self._add_buffer(line)
            enc_data.append(crypto.aes.ige256_encrypt(line, AES_PASS, VI_KEY))
        async with aiofiles.open(self.ses_path_enc, 'wb') as wer:
            await wer.writelines(enc_data)

    async def decrypt_data(self):
        ''' decrpts encrypted file '''
        async with aiofiles.open(self.ses_path_enc, 'rb') as dec:
            data = await dec.readlines()
        dec_data = []
        for line in data:
            dec_data.append(crypto.aes.ige256_decrypt(line, AES_PASS, VI_KEY).strip())
        async with aiofiles.open(self.ses_path, 'wb') as wer:
            await wer.writelines(dec_data)

    async def load_session(self, client: Client):
        ''' loadz session from telegram '''
        save: types.Message = await client.get_messages(LOG_ID, self.tg_save)
        doc = save.document
        if doc and doc.file_name == self.file + '.enc':
            await client.download_media(
                message=save,
                file_name=self.ses_path_enc,
                block=True,
            )
            await self.decrypt_data()
            return True
        return False

    async def save_session(self, client: Client):
        ''' exports file to telegram '''
        if not os.path.isfile(self.ses_path):
            # Try a Logging
            return False
        await self.encrypt_data()
        await client.edit_message_media(
            chat_id=LOG_ID,
            message_id=self.tg_save,
            media=types.InputMediaDocument(
                media=self.ses_path_enc,
                thumb=self.jthumb
            )
        )
        return True

    async def get_json(self, client: Client):
        ''' returns json data in a file '''
        if not os.path.isfile(self.ses_path):
            is_save = await self.load_session(client)
            if not is_save:
                return {}
        with open(self.ses_path, 'rb') as j_s:
            data = json.load(j_s)
        return data

    async def write_json(self, client: Client, data: dict):
        ''' writes a json data to file [this may flush entire file]'''
        with open(self.ses_path, 'w') as j_s:
            json.dump(data, j_s)
        return await self.save_session(client)
