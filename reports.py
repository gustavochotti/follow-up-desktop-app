# reports.py
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from config import FISK_BLUE, SUCCESS_GREEN, FISK_RED

class ReportGenerator:
    def get_filtered_data(self, df, period, start_date_str, end_date_str, att_filter, course_filter):
        today = datetime.date.today()
        start_date = None
        end_date = pd.to_datetime(today)

        if period == "custom":
            if start_date_str:
                start_date = pd.to_datetime(start_date_str, format='%d/%m/%Y')
            if end_date_str:
                end_date = pd.to_datetime(end_date_str, format='%d/%m/%Y')
        else:
            if period == "7_days": start_date = today - datetime.timedelta(days=7)
            elif period == "15_days": start_date = today - datetime.timedelta(days=15)
            elif period == "30_days": start_date = today - datetime.timedelta(days=30)
            elif period == "60_days": start_date = today - datetime.timedelta(days=60)
            elif period == "90_days": start_date = today - datetime.timedelta(days=90)
            elif period == "this_month": start_date = today.replace(day=1)
            
            if start_date:
                start_date = pd.to_datetime(start_date)

        df_filtered = df.copy()
        if start_date is not None:
            df_filtered = df_filtered[df_filtered['visit_date_dt'] >= start_date]
        if end_date is not None:
            df_filtered = df_filtered[df_filtered['visit_date_dt'] < (end_date + pd.Timedelta(days=1))]
        
        if att_filter != "Todos":
            df_filtered = df_filtered[df_filtered['attended_by'] == att_filter]
        if course_filter != "Todos":
            df_filtered = df_filtered[df_filtered['course'] == course_filter]
            
        return df_filtered

    def update_visits_enrollments_chart(self, ax, fig, df):
        ax.clear()
        if df.empty:
            ax.text(0.5, 0.5, "Sem dados no período", ha='center', va='center')
        else:
            total_visitas = len(df)
            total_matriculas = len(df[df['status'] == 'Fechou matrícula'])
            data = {'Visitas': total_visitas, 'Matrículas': total_matriculas}
            colors = [FISK_BLUE, SUCCESS_GREEN]
            ax.bar(data.keys(), data.values(), color=colors)
            for i, v in enumerate(data.values()):
                ax.text(i, v + (total_visitas * 0.02), str(v), ha='center', fontweight='bold')
        ax.set_title('Visitas vs. Matrículas')
        ax.set_ylabel('Quantidade')
        ax.set_ylim(bottom=0)
        fig.canvas.draw()

    def update_status_distribution_chart(self, ax, fig, df):
        ax.clear()
        if df.empty:
            ax.text(0.5, 0.5, "Sem dados no período", ha='center', va='center')
        else:
            status_counts = df['status'].value_counts()
            ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
            ax.axis('equal')
        ax.set_title('Distribuição por Status')
        fig.canvas.draw()

    def update_lead_source_chart(self, ax, fig, df):
        ax.clear()
        if df.empty:
            ax.text(0.5, 0.5, "Sem dados no período", ha='center', va='center')
        else:
            source_counts = df['how_found'].value_counts().sort_values(ascending=True)
            source_counts.plot(kind='barh', ax=ax, color=FISK_RED)
            for index, value in enumerate(source_counts):
                ax.text(value, index, f' {value}', va='center', fontweight='bold')
        ax.set_title('Origem dos Leads')
        ax.set_xlabel('Quantidade')
        ax.set_ylabel('')
        fig.canvas.draw()

    def update_top_courses_chart(self, ax, fig, df):
        ax.clear()
        if df.empty:
            ax.text(0.5, 0.5, "Sem dados no período", ha='center', va='center')
        else:
            course_counts = df['course'].value_counts().nlargest(5).sort_values(ascending=False)
            course_counts.plot(kind='bar', ax=ax, color=FISK_BLUE)
            ax.tick_params(axis='x', rotation=15)
            for i, v in enumerate(course_counts):
                ax.text(i, v + (course_counts.max() * 0.02), str(v), ha='center', fontweight='bold')
        ax.set_title('Cursos Mais Procurados')
        ax.set_ylabel('Quantidade')
        fig.canvas.draw()