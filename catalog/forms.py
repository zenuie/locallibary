from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _  # 自動翻譯
import datetime  # for checking renewal date range.


# 續借模組
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 1970, -1)),
                                   help_text="輸入你要延長的時間，預設三個禮拜(最多延長四個禮拜)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # 判斷使用者輸入時間有沒有比現在時間更早
        if data < datetime.date.today():
            raise ValidationError(_('輸入的日期不能比現在時間更早'))

        # 確認輸入時間沒超過最大值(4個禮拜)
        elif data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('最多只能延期4個禮拜喔'))

        # 記得永遠都要回傳格式化data
        return data
