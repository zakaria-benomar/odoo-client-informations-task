from odoo import models, fields, api
import requests
from lxml import html
from odoo import exceptions



class client(models.Model):
    _inherit = 'res.partner'
    denomination = fields.Char('Dénomination')
    rc = fields.Char('RC')
    idf = fields.Char('IF')
    ice = fields.Char('ICE')
    patente = fields.Char('Patente')

    @api.multi
    def open_wizard(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'client.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_denomination': self.name}
        }


class informations(models.TransientModel):
    _name = 'client.wizard'

    denomination = fields.Char('Dénomination')
    rc = fields.Char('RC')
    idf = fields.Char('IF')
    ice = fields.Char('ICE')
    patente = fields.Char('Patente')
    json_result = fields.One2many("client.informations", "informations")

    @api.multi
    def get_if(self, ice):
        url = "https://simpl-recherche.tax.gov.ma/RechercheEntreprise/result"
        payload = {"param['type']": "ICE",
                   "param['criteria']": ice,  # numeroIce
                   "param['btnType']": "Rechercher"
                   }
        r = requests.post(url, payload)
        root = html.fromstring(r.content)

        for result in root.cssselect('input#mCriteria'):
            if result.name == "param['ifu']":
                return result.value

        return

    @api.multi
    def get_company_infos(self, denomination):
        output = {}
        denomination = denomination.replace(" ", "%20")
        url = "https://www.directinfo.ma/directinfo-backend/api/queryDsl/search/"
        r = requests.get(url + denomination)
        results = r.json()
        # get only json info [[{jsoninfo}], count]
        results = results[0]

        if len(results) <= 0:
            # if there's no result
            output = {}

        else:
            # if there's 1 OR many results
            for result in results:
                key = results.index(result)
                output[key] = {
                    'denomination': result['denomination'],
                    'city': result['libelle'],
                    'ice': result['numeroIce'],
                    'rc': result['numeroRc'],
                    'idf': self.get_if(result['numeroIce'])
                }

        return output

    @api.multi
    def chercher(self):
        self.json_result.unlink()
        result_json = self.get_company_infos(self.denomination)
        if len(result_json) == 0:

            raise exceptions.Warning(' Dénomination non trouvée, veuillez réessayer.')
            self.ice = None
            self.rc = None
            self.idf = None

        else:
            for key, value in result_json.items():
                vals = {'denomination': value['denomination'],
                        'rc': value['rc'],
                        'idf': value['idf'],
                        'ice': value['ice'],
                        'patente': ''}
                self.json_result = [(0, 0, vals)]
                self.ice = None
                self.rc = None
                self.idf = None

            if len(result_json) == 1:
                self.ice = self.json_result.ice
                self.rc = self.json_result.rc
                self.idf = self.json_result.idf

        return {
            "type": "set_scrollTop",
        }

    @api.one
    def enregistrer_func(self):
        for record in self.env['res.partner'].browse(self._context.get('active_ids', [])):
            record.denomination = self.denomination
            record.rc = self.rc
            record.idf = self.idf
            record.ice = self.ice
            record.patente = self.patente




class infos_json(models.TransientModel):
    _name = "client.informations"
    denomination = fields.Char('Dénomination')
    rc = fields.Char('RC')
    idf = fields.Char('IF')
    ice = fields.Char('ICE')
    patente = fields.Char('Patente')
    informations = fields.Many2one("client.wizard")

    @api.multi
    def appliquer_func(self):
        self.informations.rc = self.rc
        self.informations.idf = self.idf
        self.informations.ice = self.ice
        self.informations.patente = self.patente

        return {
            "type": "set_scrollTop",
        }







