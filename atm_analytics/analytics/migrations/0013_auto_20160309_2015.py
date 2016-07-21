# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import atm_analytics.analytics.models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0012_remove_atmcase_cash_replacement_schedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='atmerroreventviewer',
            options={'verbose_name': 'EventViewer Error', 'verbose_name_plural': 'EventViewer Errors'},
        ),
        migrations.AlterModelOptions(
            name='atmerrorxfs',
            options={'verbose_name': 'XFS Error', 'verbose_name_plural': 'XFS Errors'},
        ),
        migrations.AlterModelOptions(
            name='case',
            options={'verbose_name': 'Case'},
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='atm_location',
            field=models.ManyToManyField(help_text='ATM location', related_name='locations', to='companies.CompanyAtmLocation'),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='operating_system',
            field=models.CharField(help_text='Operating system', max_length=1, choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')]),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='other_log',
            field=models.FileField(help_text='Another type of log?', null=True, upload_to=atm_analytics.analytics.models.get_atm_other_log_attachment_path, blank=True),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='person_name_journal_virtual',
            field=models.CharField(help_text='Name of the person who facilitates the virtual Journal', max_length=255),
        ),
        migrations.AlterField(
            model_name='atmcase',
            name='software',
            field=models.CharField(help_text='Software', max_length=1, choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', 'Other XFS')]),
        ),
        migrations.AlterField(
            model_name='atmerroreventviewer',
            name='color',
            field=models.CharField(help_text='Error color', max_length=1, verbose_name='Color', choices=[(b'#008000', 'green'), (b'#FF0000', 'red'), (b'#FF9300', 'orange')]),
        ),
        migrations.AlterField(
            model_name='atmerroreventviewer',
            name='description',
            field=models.CharField(help_text='Description of error', max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='atmerroreventviewer',
            name='identifier',
            field=models.CharField(help_text='Unique identifier of the error', unique=True, max_length=255, verbose_name='Identifier', db_index=True),
        ),
        migrations.AlterField(
            model_name='atmerroreventviewer',
            name='operating_system',
            field=models.CharField(help_text='ATM Operating System', max_length=1, verbose_name='Operating System', choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')]),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='color',
            field=models.CharField(help_text='Error color', max_length=1, verbose_name='Color', choices=[(b'#008000', 'green'), (b'#FF0000', 'red'), (b'#FF9300', 'orange')]),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='description',
            field=models.CharField(help_text='Description of error', max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='fault',
            field=models.CharField(help_text='Who is guilty?', max_length=1, verbose_name='Guilt', choices=[(b'0', 'user'), (b'1', 'bank'), (b'1', 'transporting company'), (b'3', 'anonymous')]),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='hardware',
            field=models.CharField(help_text='ATM hardware', max_length=1, verbose_name='Hardware', choices=[(b'0', b'Diebold'), (b'1', b'Wincor Nixdorf'), (b'2', b'NCR'), (b'3', b'Triton')]),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='identifier',
            field=models.CharField(help_text='Unique identifier of the error', unique=True, max_length=255, verbose_name='Identifier', db_index=True),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='operating_system',
            field=models.CharField(help_text='ATM Operating System', max_length=1, verbose_name='Operating System', choices=[(b'0', b'Windows XP'), (b'1', b'Windows 7'), (b'2', b'Windows 8')]),
        ),
        migrations.AlterField(
            model_name='atmerrorxfs',
            name='software',
            field=models.CharField(help_text='ATM software', max_length=1, verbose_name='Software', choices=[(b'0', b'Agilis'), (b'1', b'APTRA'), (b'2', b'Procash/probase'), (b'3', b'JAM Dynasty'), (b'4', b'Kal'), (b'5', 'Other XFS')]),
        ),
        migrations.AlterField(
            model_name='atmeventviewerevent',
            name='event_date',
            field=models.DateTimeField(verbose_name='Date of the event'),
        ),
        migrations.AlterField(
            model_name='case',
            name='bank',
            field=models.ForeignKey(related_name='bank_cases', to='companies.Bank', help_text='Bank'),
        ),
        migrations.AlterField(
            model_name='case',
            name='created_date',
            field=models.DateField(help_text='Creation date of the case', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.TextField(help_text='Extra brief description of the case', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='missing_amount',
            field=models.DecimalField(help_text='Estimated amount missing', max_digits=19, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='case',
            name='missing_amount_currency',
            field=models.CharField(help_text='Currency', max_length=3, choices=[(b'0', b'afghani - \xd8\x8b (AFN) | Afghanistan'), (b'1', b'lek - L (ALL) | Albania'), (b'2', b'euro - \xe2\x82\xac (EUR) | Germany'), (b'3', b'euro - \xe2\x82\xac (EUR) | Andorra'), (b'4', b'kuanza de Angola - Kz (AOA) | Angola'), (b'5', b'rial saud\xc3\xad - \xd8\xb1.\xd8\xb3 (SAR) | Saudi Arabia'), (b'6', b'dinar - \xd8\xaf.\xd8\xac (DZD) | Algeria'), (b'7', b'peso argentino - $ (ARS) | Argentina'), (b'8', b'dram armenio - \xc2\xa0 (AMD) | Armenia'), (b'9', b'flor\xc3\xadn arubano - \xc6\x92 (AWG) | Aruba'), (b'10', b'd\xc3\xb3lar australiano - $ (AUD) | Australia'), (b'11', b'euro - \xe2\x82\xac (EUR) | Austria'), (b'12', b'manat azerbayano - \xc2\xa0 (AZN) | Azerbaijan'), (b'13', b'd\xc3\xb3lar de las Bahamas - $ (BSD) | Bahamas'), (b'14', b'taka de Banglad\xc3\xa9s - \xe0\xa7\xb3 (BDT) | Bangladesh'), (b'15', b'd\xc3\xb3lar de las Barbados - $ (BBD) | Barbados'), (b'16', b'dinar de Bar\xc3\xa9in - .\xd8\xaf.\xd8\xa8 (BHD) | Bahrain'), (b'17', b'd\xc3\xb3lar belice\xc3\xb1o - $ (BZD) | Belize'), (b'18', b'rublo bielorruso - Br (BYR) | Belarus'), (b'19', b'kiat de Birmania - K (MMK) | Myanmar'), (b'20', b'boliviano - Bs. (BOB) | Bolivia'), (b'21', b'marco convertible de Bosnia y Herzegovina - KM (BAM) | Bosnia and Herzegovina'), (b'22', b'pula de Botsuana - P (BWP) | Botswana'), (b'23', b'real brasile\xc3\xb1o - R$ (BRL) | Brazil'), (b'24', b'd\xc3\xb3lar de Brunei - $ (BND) | Brunei'), (b'25', b'leva b\xc3\xbalgaro - \xd0\xbb\xd0\xb2 (BGN) | Bulgaria'), (b'26', b'franco CFA - Fr (XOF) | Burkina Faso'), (b'27', b'franco burund\xc3\xa9s - Fr (BIF) | Burundi'), (b'28', b'gultrum butan\xc3\xa9s - Nu. (BTN) | Bhutan'), (b'29', b'euro - \xe2\x82\xac (EUR) | Belgium'), (b'30', b'escudo de Cabo Verde - Esc, $ (CVE) | Cape Verde'), (b'31', b'riel camboyano - \xe1\x9f\x9b (KHR) | Cambodia'), (b'32', b'd\xc3\xb3lar canadiense - $ (CAD) | Canada'), (b'33', b'rial catar\xc3\xad - \xd8\xb1.\xd9\x82 (QAR) | Qatar'), (b'34', b'franco CFA - Fr (XAF) | Chad'), (b'35', b'peso chileno - $ (CLP) | Chile'), (b'36', b'yuan, renminbi - \xc2\xa5, \xe5\x85\x83 (CNY) | China'), (b'37', b'euro - \xe2\x82\xac (EUR) | Cyprus'), (b'38', b'euro - \xe2\x82\xac (EUR) | Vatican CITY'), (b'39', b'peso colombiano - $ (COP) | Colombia'), (b'40', b'franco comorano - Fr (KMF) | Comoros'), (b'41', b'won norcoreano - \xe2\x82\xa9 (KPW) | North Korea'), (b'42', b'won surcoreano - \xe2\x82\xa9 (KRW) | South Korea'), (b'43', b'franco CFA - Fr (XOF) | Ivory Coast'), (b'44', b'col\xc3\xb3n costarrique\xc3\xb1o - \xe2\x82\xa1 (CRC) | Costa Rica'), (b'45', b'kuna croata - kn (HRK) | Croatia'), (b'46', b'peso cubano - $ (CUP) | Cuba'), (b'47', b'flor\xc3\xadn de las Antillas Neerlandesas - \xc6\x92 (ANG) | Cura\xc3\xa7ao'), (b'48', b'corona danesa - kr (DKK) | Denmark'), (b'49', b'libra egipcia - \xc2\xa3, \xd8\xac.\xd9\x85 (EGP) | Egypt'), (b'50', b'col\xc3\xb3n salvadore\xc3\xb1o - \xe2\x82\xa1 (SVC) | El Salvador'), (b'51', b'd\xc3\xadrham - \xd8\xaf.\xd8\xa5 (AED) | United Arab Emirates'), (b'52', b'nakfa de Eritrea - Nfk (ERN) | Eritrea'), (b'53', b'euro - \xe2\x82\xac (EUR) | Slovakia'), (b'54', b'euro - \xe2\x82\xac (EUR) | Slovenia'), (b'55', b'euro - \xe2\x82\xac (EUR) | Spain'), (b'56', b'd\xc3\xb3lar micronesio - $ (nenhum) | Federated States of Micronesia'), (b'57', b'd\xc3\xb3lar estadounidense - $ (USD) | United States'), (b'58', b'euro - \xe2\x82\xac (EUR) | Estonia'), (b'59', b'bir - Br (ETB) | Ethiopia'), (b'60', b'peso filipino - \xe2\x82\xb1 (PHP) | Philippines'), (b'61', b'euro - \xe2\x82\xac (EUR) | Finland'), (b'62', b'euro - \xe2\x82\xac (EUR) | France'), (b'63', b'franco CFA - Fr (XAF) | Gabon'), (b'64', b'dalasi gambiano - D (GMD) | Gambia'), (b'65', b'cedi de Gana - \xe2\x82\xb5 (GHS) | Ghana'), (b'66', b'lari georgiano - \xe1\x83\x9a (GEL) | Georgia'), (b'67', b'libra de Gibraltar - \xc2\xa3 (GIP) | Gibraltar'), (b'68', b'euro - \xe2\x82\xac (EUR) | Greece'), (b'69', b'quetzal - Q (GTQ) | Guatemala'), (b'70', b'franco guineano - Fr (GNF) | Guinea'), (b'71', b'franco CFA - Fr (XAF) | Equatorial Guinea'), (b'72', b'franco CFA - Fr (XOF) | Guinea Bissau'), (b'73', b'gurde - G (HTG) | Haiti'), (b'74', b'lempira - L (HNL) | Honduras'), (b'75', b'forinto - Ft (HUF) | Hungary'), (b'76', b'rupia india - \xc2\xa0 (INR) | India'), (b'77', b'rupia indonesia - Rp (IDR) | Indonesia'), (b'78', b'dinar irak\xc3\xad - \xd8\xb9.\xd8\xaf (IQD) | Iraq'), (b'79', b'euro - \xe2\x82\xac (EUR) | Ireland'), (b'80', b'rial iran\xc3\xad - \xef\xb7\xbc (IRR) | Iran'), (b'81', b'corona islandesa kr (ISK) | Iceland'), (b'82', b'd\xc3\xb3lar de las Islas Caim\xc3\xa1n - $ (KYD) | Cayman Islands'), (b'83', b'd\xc3\xb3lar salomonense - $ (SBD) | Solomon Islands'), (b'84', b'nuevo s\xc3\xa9quel - \xe2\x82\xaa (ILS) | Israel'), (b'85', b'euro - \xe2\x82\xac (EUR) | Italy'), (b'86', b'd\xc3\xb3lar jamaicano - $ (JMD) | Jamaica'), (b'87', b'yen - \xc2\xa5 (JPY) | Japan'), (b'88', b'dinar jordano - \xd8\xaf.\xd8\xa7 (JOD) | Jordan'), (b'89', b'tengue kazajo - \xe2\x82\xb8 (KZT) | Kazakhstan'), (b'90', b'chel\xc3\xadn keniano - Sh (KES) | Kenya'), (b'91', b'som kirgu\xc3\xads - \xd0\xbb\xd0\xb2 (KGS) | Kyrgyzstan'), (b'92', b'dinar kuwait\xc3\xad - \xd8\xaf.\xd9\x83 (KWD) | Kuwait'), (b'93', b'kip - \xe2\x82\xad (LAK) | Laos'), (b'94', b'loti de Lesoto - L (LSL) | Lesotho'), (b'95', b'lats - Ls (LVL) | Latvia'), (b'96', b'd\xc3\xb3lar liberiano - $ (LRD) | Liberia'), (b'97', b'dinar libio - \xd9\x84.\xd8\xaf (LYD) | Libya'), (b'98', b'litas - Lt (LTL) | Lithuania'), (b'99', b'euro - \xe2\x82\xac (EUR) | Luxembourg'), (b'100', b'libra libanesa - \xd9\x84.\xd9\x84 (LBP) | Lebanon'), (b'101', b'pataca de Macao - P (MOP) | Macao'), (b'102', b'denar - \xd0\xb4\xd0\xb5\xd0\xbd (MKD) | Macedonia'), (b'103', b'ariari - Ar (MGA) | Madagascar'), (b'104', b'ringit - RM (MYR) | Malaysia'), (b'105', b'kuacha de Malaui - MK (MWK) | Malawi'), (b'106', b'rufiya - .\xde\x83 (MVR) | Maldives'), (b'107', b'franco CFA - Fr (XOF) | Mali'), (b'108', b'euro - \xe2\x82\xac (EUR) | Malta'), (b'109', b'd\xc3\xadrham - \xd8\xaf.\xd9\x85. (MAD) | Morocco'), (b'110', b'rupia de Mauricio - \xe2\x82\xa8 (MUR) | Mauricio'), (b'111', b'uguiya - UM (MRO) | Mauritania'), (b'112', b'leu moldavo - L (MDL) | Moldova'), (b'113', b'tugrik mongol - \xe2\x82\xae (MNT) | Mongolia'), (b'114', b'euro - \xe2\x82\xac (EUR) | Montenegro'), (b'115', b'metical - MT (MZN) | Mozambique'), (b'116', b'peso mexicano - $ (MXN) | Mexico'), (b'117', b'euro - \xe2\x82\xac (EUR) | Monaco'), (b'118', b'd\xc3\xb3lar de Namibia - $ (NAD) | Namibia'), (b'119', b'd\xc3\xb3lar nauruano - $ (Nenhum) | Nauru'), (b'120', b'rupia nepal\xc3\xad - \xe2\x82\xa8 (NPR) | Nepal'), (b'121', b'c\xc3\xb3rdoba nicarag\xc3\xbcense - C$ (NIO) | Nicaragua'), (b'122', b'naira nigeriano - \xe2\x82\xa6 (NGN) | Nigeria'), (b'123', b'corona noruega - kr (NOK) | Norway'), (b'124', b'franco CFP - Fr (XPF) | New Caledonia'), (b'125', b'd\xc3\xb3lar de Nueva Zelanda - $ (NZD) | New Zealand'), (b'126', b'franco CFA - Fr (XOF) | Niger'), (b'127', b'rial de Om\xc3\xa1n - \xd8\xb1.\xd8\xb9. (OMR) | Oman'), (b'128', b'balboa paname\xc3\xb1o - B/. (PAB) | Panama'), (b'129', b'kina - K (PGK) | Papua New Guinea'), (b'130', b'rupia pakistan\xc3\xad - \xe2\x82\xa8 (PKR) | Pakistan '), (b'131', b'guaran\xc3\xad paraguayo - \xe2\x82\xb2 (PYG) | Paraguay'), (b'132', b'euro - \xe2\x82\xac (EUR) | Netherlands'), (b'133', b'nuevo sol peruano - S/. (PEN) | Peru'), (b'134', b'franco CFP - Fr (XPF) | French Polynesia'), (b'135', b'z\xc5\x82\xc3\xb3ti - z\xc5\x82 (PLN) | Poland'), (b'136', b'euro - \xe2\x82\xac (EUR) | Portugal'), (b'137', b'libra esterlina - \xc2\xa3 (GBP) | United Kingdom'), (b'138', b'franco CFA - Fr (XAF) | Central African Republic'), (b'139', b'corona checa - K\xc4\x8d (CZK) | Czech Republic'), (b'140', b'franco CFA - Fr (XAF) | Republic of the Congo'), (b'141', b'franco congole\xc3\xb1o - Fr (CDF) | Democratic Republic of the Congo'), (b'142', b'peso dominicano - $ (DOP) | Dominican Republic'), (b'143', b'franco ruand\xc3\xa9s - Fr (RWF) | Rwanda'), (b'144', b'leu rumano - L (RON) | Romania'), (b'145', b'rublo - \xd1\x80\xd1\x83\xd0\xb1. (RUB) | Russia'), (b'146', b'tala - T (WST) | Samoa'), (b'147', b'd\xc3\xb3lar del Caribe Oriental - $ (XCD) | Saint Kitts and Nevis'), (b'148', b'euro - \xe2\x82\xac (EUR) | San Marino'), (b'149', b'd\xc3\xb3lar del Caribe Oriental - $ (XCD) | Saint Vincent and the Grenadines'), (b'150', b'd\xc3\xb3lar del Caribe Oriental - $ (XCD) | Saint Lucia'), (b'151', b'dobra - Db (STD) | Sao Tome and Principe'), (b'152', b'rupia seychellense - \xe2\x82\xa8 (SCR) | Seychelles'), (b'153', b'franco CFA - Fr (XOF) | Senegal'), (b'154', b'dinar serbio - \xd0\xb4\xd0\xb8\xd0\xbd.\xc2\xa0o\xc2\xa0din. (RSD) | Serbia'), (b'155', b'leona - Le (SLL) | Sierra Leone'), (b'156', b'd\xc3\xb3lar singapurense - $ (SGD) | Singapore'), (b'157', b'libra siria - \xc2\xa3\xc2\xa0o\xc2\xa0\xd9\x84.\xd8\xb3 (SYP) | Syria'), (b'158', b'chel\xc3\xadn somal\xc3\xad - Sh (SOS) | Somalia'), (b'159', b'rupia ceilandesa - Rs (LKR) | Sri Lanka'), (b'160', b'lilangeni - L (SZL) | Swaziland'), (b'161', b'rand - R (ZAR) | South Africa'), (b'162', b'libra sudanesa - \xc2\xa3 (SDG) | Sudan'), (b'163', b'libra sursudanesa - \xc2\xa3 (SSP) | South Sudan'), (b'164', b'corona sueca - kr (SEK) | Sweden'), (b'165', b'franco suizo - Fr (CHF) | Switzerland'), (b'166', b'd\xc3\xb3lar surinam\xc3\xa9s - $ (SRD) | Suriname'), (b'167', b'bat - \xe0\xb8\xbf (THB) | Thailand'), (b'168', b'nuevo d\xc3\xb3lar de Taiw\xc3\xa1n - $ (TWD) | Taiwan'), (b'169', b'chel\xc3\xadn tanzaniano - Sh (TZS) | Tanzania'), (b'170', b'somoni - \xd0\x85\xd0\x9c (TJS) | Tajikistan'), (b'171', b'franco CFA - Fr (XOF) | Togo'), (b'172', b'paanga - T$ (TOP) | Tonga'), (b'173', b'd\xc3\xb3lar trinitense - $ (TTD) | Trinidad and Tobago'), (b'174', b'manat turcomano - m (TMT) | Turkmenistan'), (b'175', b'lira turca - \xc2\xa0 (TRY) | Turkey'), (b'176', b'dinar tunecino - \xd8\xaf.\xd8\xaa (TND) | Tunisia'), (b'177', b'grivna - \xe2\x82\xb4 (UAH) | Ukraine'), (b'178', b'chel\xc3\xadn ugand\xc3\xa9s - Sh (UGX) | Uganda'), (b'179', b'peso uruguayo - $ (UYU) | Uruguay'), (b'180', b'sum - \xd0\xbb\xd0\xb2 (UZS) | Uzbekistan'), (b'181', b'vatu do Vanuatu - Vt (VUV) | Vanuatu'), (b'182', b'bol\xc3\xadvar fuerte - Bs F (VEF) | Venezuela'), (b'183', b'dong - \xe2\x82\xab (VND) | Vietnam'), (b'184', b'rial yemen\xc3\xad - \xef\xb7\xbc (YER) | Yemen'), (b'185', b'franco yibutiano - Fr (DJF) | Djibouti'), (b'186', b'kuacha zambiano - ZK (ZMK) | Zambia'), (b'187', b'd\xc3\xb3lar zimbabuense - $ (ZWL) | Zimbabwe')]),
        ),
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(help_text='Case name', max_length=255),
        ),
        migrations.AlterField(
            model_name='case',
            name='number',
            field=models.IntegerField(help_text='Case number', db_index=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='priority',
            field=models.CharField(help_text='Importance of the case', max_length=1, choices=[(b'0', 'low'), (b'1', 'medium'), (b'2', 'high')]),
        ),
        migrations.AlterField(
            model_name='case',
            name='status',
            field=models.CharField(default=b'0', help_text='Case status', max_length=1, choices=[(b'0', 'open'), (b'1', 'close')]),
        ),
    ]
