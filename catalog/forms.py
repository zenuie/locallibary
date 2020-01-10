from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


# 續借模組
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="輸入你要延長的時間，預設三個禮拜(最多延長四個禮拜)")

    def clean_renewal_data(self):
        data = self.cleaned_data['renewal_date']

        # 判斷使用者輸入時間有沒有比現在時間更早
        if data < datetime.date.today():
            raise ValidationError(_('錯誤的時間，您輸入的時間為過去'))

        # 確認輸入時間沒超過最大值(4個禮拜)
        elif data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('已超出範圍，請輸入正確時間'))

        # 記得永遠都要回傳清理data
        return data
